"""
personal getDates.py config file

"""

# don't forget to rename this file to config.py after editing it for the first time

# put in here your email adress used to login to foodsharing.de
email_adress = 'my@dre.ss'

# put in here your password used to login to foodsharing.de
# /!\ this is saved in clear text  /!\ 
# you can also leave this empty if you want, but you will be asked on runtime
password = '' 

# duration of generated event in minutes 
DELTAMINUTES = 30

# the dates from foodsharing.de do not have a year mentioned. Set the proper year for the events here
THISYEAR = 2017

# only print the new event to screen instead of creating a event in the calendar for testing purposes 
testmode = False
