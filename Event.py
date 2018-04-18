# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.

import quickstart
import PartyBuddy

myEventId = ''


# todo: date overflow,
# todo: update - theme (description), attendees, reminders
def create_event(location, date, time):
    endTime = str((int(time) + 5) % 24)
    # if (int(time) + 5) > 24:
    #     endDate = str(int(date[-2:0]) + 1)
    # else:
    #     endDate = date
    event = {
        'summary': 'My Party',
        'location': location,
        'description': 'COME PARTY!!!1!',
        'start': {
            'dateTime': date + 'T' + time + ':00:00+01:00',
            'timeZone': 'Europe/London',
        },
        'end': {
            'dateTime': date + 'T' + endTime + ':00:00+01:00',
            'timeZone': 'Europe/London',
        },
        'attendees': [
            {'email': 'lpage@example.com'},
            {'email': 'sbrin@example.com'},
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


def update_event(name):
    # First retrieve the event from the API.
    event = quickstart.service.events().get(calendarId='aei1.2018@flightofstairs.org', eventId=myEventId).execute()

    email = PartyBuddy.contacts[name]
    event['attendees'].append({'email': email})

    quickstart.service.events().update(calendarId='aei1.2018@flightofstairs.org', eventId=myEventId, body=event).execute()
