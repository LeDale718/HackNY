from flask import Flask, request
from flask_cors import CORS

import httplib2
import os

from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import dateutil.parser

app = Flask(__name__)
CORS(app)

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret_new.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

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
        print('Storing credentials to ' + credential_path)
    return credentials


def add_work_study_time(event_name, event_hours, event_list, my_service):
    hours = event_hours
    for event in event_list:
            start_time = dateutil.parser.parse(event['start']['dateTime'])
            end_time = dateutil.parser.parse(event['end']['dateTime'])
            # time_to_finish = end_time - start_time

            if hours > 0:
                    my_event = {
                        'summary': 'Study for ' + event_name,
                        'start': {
                            'dateTime': end_time.isoformat(),
                            'timeZone': event['start']['timeZone'],
                        },
                        'end':{
                            'dateTime': (end_time + datetime.timedelta(minutes=60)).isoformat(),
                            'timeZone': event['end']['timeZone'],
                        },
                    }
                    # new_event = my_service.events().insert(calendarId='primary', body=my_event).execute()
                    print(event['summary'])
                    print(my_event)
                    hours = hours - 1
                    print("Hours : " + str(hours))

    return


@app.route('/add_event/', methods=['GET', 'POST'])
def add_event():
    print("Hello")
    event_title = request.form['event_title']
    print(event_title)
    location = request.form['event_location']
    # event_start = request.form['event_start']
    event_start = '2018-04-11T011:34'
    event_end = '2018-04-11T12:34'

    until_time = dateutil.parser.parse(event_start).isoformat() + 'Z'
    print(until_time)
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(now)
    print('Getting the upcoming events until event')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, timeMax=until_time, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    # print(len(events))
    #
    # free_request = {
    #     "timeMax": "2018-04-11T11:34:00Z",
    #     "items": [
    #             {
    #              "id": "primary"
    #             }
    #         ],
    #     "timeMin": "2018-04-08T11:34:00Z"
    # }
    #
    # freeResult = service.freebusy().query(free_request)

    real_event = {
        'summary': event_title,
        'location': location,
        'start': {
            'dateTime': dateutil.parser.parse(event_start).isoformat(),
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': (dateutil.parser.parse(event_end)).isoformat(),
            'timeZone': 'America/New_York',
        },
    }

    new_event = service.events().insert(calendarId='primary', body=real_event).execute()
    add_work_study_time(event_title, 5, events, service)

    return


if __name__ == '__main__':
    app.run(host='0.0.0.0')

