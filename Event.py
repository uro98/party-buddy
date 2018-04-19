# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.

import quickstart
import PartyBuddy
from dateconversion import end_time

myEventId = ''


# todo: date overflow,
# todo: update - theme (description), attendees, reminders
def create_event(location, date, time):
    event = {
        'summary': 'My Party',
        'location': location,
        'description': 'COME PARTY!!!1!',
        'start': {
            'dateTime': date + 'T' + time + ':00:00+01:00',
            'timeZone': 'Europe/London',
        },
        'end': {
            'dateTime': end_time(date, time).strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Europe/London',
        },
        'attendees': [
            {'email': 'aei1.2018@flightofstairs.org'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 60},
            ],
        },
    }

    event = quickstart.service.events().insert(calendarId='aei1.2018@flightofstairs.org', body=event).execute()
    global myEventId
    myEventId = event['id']
    print('Event created: %s' % (event.get('htmlLink')))


def update_event_invitees(name):
    # First retrieve the event from the API.
    event = quickstart.service.events().get(calendarId='aei1.2018@flightofstairs.org', eventId=myEventId).execute()

    email = PartyBuddy.contacts[name]
    event['attendees'].append({'email': email})

    quickstart.service.events().update(calendarId='aei1.2018@flightofstairs.org', eventId=myEventId, body=event).execute()


def update_event_description(themeNumber):
    # First retrieve the event from the API.
    event = quickstart.service.events().get(calendarId='aei1.2018@flightofstairs.org', eventId=myEventId).execute()

    event['description'] = 'Theme: ' + PartyBuddy.themes[themeNumber]

    quickstart.service.events().update(calendarId='aei1.2018@flightofstairs.org', eventId=myEventId, body=event).execute()


def update_event_location(location):
    # First retrieve the event from the API.
    event = quickstart.service.events().get(calendarId='aei1.2018@flightofstairs.org', eventId=myEventId).execute()

    event['location'] = location

    quickstart.service.events().update(calendarId='aei1.2018@flightofstairs.org', eventId=myEventId, body=event).execute()


# def update_event_date(date):
#     # First retrieve the event from the API.
#     event = quickstart.service.events().get(calendarId='aei1.2018@flightofstairs.org', eventId=myEventId).execute()
#
#     event['description'] = PartyBuddy.themes[PartyBuddy.themeNumber]
#
#     quickstart.service.events().update(calendarId='aei1.2018@flightofstairs.org', eventId=myEventId, body=event).execute()
#
#
# def update_event_time(time):
#     # First retrieve the event from the API.
#     event = quickstart.service.events().get(calendarId='aei1.2018@flightofstairs.org', eventId=myEventId).execute()
#
#     event['description'] = PartyBuddy.themes[PartyBuddy.themeNumber]
#
#     quickstart.service.events().update(calendarId='aei1.2018@flightofstairs.org', eventId=myEventId, body=event).execute()

def get_attendees_status():
    event = quickstart.service.events().get(calendarId='aei1.2018@flightofstairs.org', eventId=myEventId).execute()
    attendeesList = event['attendees']
    accepted = list(filter(lambda x: x['responseStatus'] == 'accepted', attendeesList))
    print(attendeesList)
    print(accepted)
    emails = map(lambda x: x['email'], accepted)
    return emails
