#!/usr/bin/env python3
"""
script for fetching foodsaving dates/locations from foodsharing.de
and create events for the users Google Calendar.

these files have to be in the same Folder:
- getDates.py 
- makeDate.py 
- config.py with your own credentials
- quickstart.py
- client_secret.json downloaded from the Google API Manager

stuff to install/import:
- pip
    apt-get install python3-pip

- module bs4
    BeautifulSoup to store data pulled from html:
    apt-get install python3-bs4
    
- modules apiclient, oauth2client, httplib2
    Google API modules to access calendar:
    pip3 install --upgrade google-api-python-client
    
before running this script for the first time follow the instructions at
https://developers.google.com/google-apps/calendar/quickstart/python
and run quickstart.py to initiate the verification procedure for the 
Google Calendar.
It will (try to) open a web page where you login with your google 
account to confirm the access rights of this scipt to your calendar.
It will also set up an temporary webserver at localhost:8080, so if you 
do this on a remote box, use the parameter --noauth_local_webserver 

If quickstart.py is done it will print your next 10 entries of your main
calendar.


This script logs in to the dashboard of foodsharing.de using your 
credentials set below. Then it saves the dashboard-page locally, and 
parses it, searching for the list containing the dates 
and shops ("nächste Abholtermine") 

This data is the used to create events

/!\ Your login credentials are stored in plain text in config.py  /!\  

"""


import os 
import time
from html.parser import HTMLParser
from bs4 import BeautifulSoup # the parsed html is stored in this soup

import makeDate
import config

# execute wget quietly to login and download the dashboard page
# if you didn't set the password in config.py, you will be asked
if config.password == '':
    import getpass
    os.system(("wget -nv --post-data \'email_adress={}&password={}\' " + 
        "https://foodsharing.de/?page=dashboard")
        .format(config.email_adress, getpass.getpass(
            "foodsharing.de Login mit email " + config.email_adress + 
            ".\nPasswort:"))) 
else:
    os.system(("wget -nv --post-data \'email_adress={}&password={}\' " +
        "https://foodsharing.de/?page=dashboard")
        .format(config.email_adress, config.password)) 

# wget needs some time to get the file
time.sleep(2)

with open("index.html?page=dashboard") as fp:
    soup = BeautifulSoup(fp, "html.parser")
    #print(soup.text)

os.system("rm index.html?page=dashboard")
dates = ''

# dates are stored in a <ul> list with class = "datelist linklist"
for row in soup.find_all("ul", "datelist linklist"):
    #print(row.text)
    dates += row.text

# the dates.splitlines string has empty entries, get rid of them    
datelist = list(filter(None, dates.splitlines()))

for i in range(int(len(datelist)/2)):
    print(str(i+1) + '. Abholung: ' + datelist[2*i] + ' bei ' + datelist[2*i+1])
    makeDate.main(datelist[2*i], datelist[2*i+1])
