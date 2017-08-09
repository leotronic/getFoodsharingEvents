"""
this script uses the Google Calendar API

Python as well as your Google Account have to be set up for this.
To do this, you can look at
https://developers.google.com/google-apps/calendar/quickstart/python

"""

from __future__ import print_function
import httplib2
import os
import locale # needed for parsing german time Strings 
import sys
import datetime
import config

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


# set locale time category to german so the parser undstands the german names of months and weekdays
locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
#APPLICATION_NAME = 'Google Calendar API Python Quickstart'
APPLICATION_NAME = 'GetFoodsharingDates'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    This will open a Browser asking the user if he is willing to use the
    python script with his calendar

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('credentials gespeichert in ' + credential_path)
    return credentials

def makeEvent(timeString, location):
    """
    takes time and location name and generates an event object to send to 
    the Google calendar.
    
    """
    timeString = timeString.rstrip()
    
    
    # if "Morgen" or "Heute" is in the timeString, replace it with the format used for other days
    if timeString.startswith('Heute'):
        timeString = timeString.replace('Heute', (datetime.date.today()).strftime('%A, %d. %b'))
    elif timeString.startswith('Morgen'):
        timeString = timeString.replace('Morgen', (datetime.date.today() + datetime.timedelta(1)).strftime('%A, %d. %b'))
    
    # parse a time String like 'Donnerstag, 10. Aug, 16:00 Uhr' and set the year
    time = datetime.datetime.strptime(timeString,'%A, %d. %b, %H:%M Uhr').replace(config.THISYEAR)
        
    event = {
        'summary': 'Abholung ' + location,
        'colorId' : '10',
        'start': {
            'dateTime': time.isoformat() + '+02:00',
            'timeZone': 'Europe/Berlin',
        },
        'end': {
            'dateTime': (time + datetime.timedelta(0,0,0,0,config.DELTAMINUTES)).isoformat() + '+02:00',
            'timeZone': 'Europe/Berlin',
        },
    }

    return event

    
        
def main(timeString, location):
    """uses the Google Calendar API to create foodsaving events given
    with the timeString and location parameters.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # generate the 'newEvent'-dictionary
    newEvent = makeEvent(timeString, location)
    newStart = newEvent['start'].get('dateTime', newEvent['start'].get('date'))
        
    # ask Google for events with 'Abholung' in its summary
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=50, singleEvents=True,
        orderBy='startTime', q='Abholung').execute()
    events = eventsResult.get('items', [])
    
    # check if one of these events is already our newEvent
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        if newStart == start and newEvent['summary'] == event['summary']:
            #print(event['summary'] + ' bei ' + start + ' gibts schon. nix zu tun. (0)')
            print(event['summary'] + ' gibts schon. nix zu tun. (0)')
            return


    if config.testmode:
        print('=== Test ohne Eintrag in Kalender ===\ndieser Event _würde_ jetzt eingetragen werden:\n')
        print(newEvent)
    else:
        event = service.events().insert(calendarId='primary', body=newEvent).execute()
        print(newEvent['summary'] + ' am ' + newStart + ', Abholung eingetragen (+)')

# this script normally receives its data from getDates.py
if __name__ == '__main__':
    if len(sys.argv) <= 1:
        main('Heute, 16:00 Uhr', '+++Testbetrieb+++')
    else:
        main(sys.argv[0], sys.argv[1])
