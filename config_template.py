"""
personal getDates.py config file

"""

# don't forget to rename this file to config.py after editing it for the first time

# put in here your email adress used to login to foodsharing.de
email_adress = ''

# put in here your password used to login to foodsharing.de
# /!\ this is saved in clear text  /!\ 
# you can also leave this empty if you want, but you will be asked on runtime
password = '' 

# duration of generated event in minutes 
deltaMinutes = 30

# python3 style format string for the 'summary' entry of the event. 
# the '{}' will be replaced with the location string
summaryFormat = 'Abholung {}'

# Google Calendars Color ID string to set the color for the event displayed
# E.g. 10 is green
# The only color chart i found was here: https://eduardopereira.pt/wp-content/uploads/2012/06/google_calendar_api_event_color_chart.png
colorId = '10'

# the dates from foodsharing.de do not have a year mentioned. Set the proper year for the events here
thisYear = 2017

# only print the new event to screen instead of creating a event in the calendar for testing purposes 
testmode = False
