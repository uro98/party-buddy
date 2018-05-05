# party-buddy

This Alexa skill allows you to connect to your Google Calendar to create an event, invite people to the event and send them notifications. It can also let you know who is coming, suggest party themes/playlists/cocktails and allow you to create a shopping list for your party.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

#### Flask-Ask

In PyCharm, go to File -> Settings -> Project: party-buddy -> Project Interpreter and click the green plus button, search for Flask-Ask and click install package.

#### ngrok

Download ngrok.

#### Alexa Skills Kit

Create a new skill on the Alexa Skills Kit Developer Console. Click JSON Editor under Interaction Model and drop the `model.json` file from this repo into the editor. This will set up all the intents and slot types. Click Save Model at the top then click Build Model.

Click Endpoint and select HTTPS as the Service Endpoint Type. This is where ngrok comes in, open ngrok and type `ngrok http 5000`, then copy the HTTPS URL under Forwarding. Paste this URL under Default Region in Endpoint on the Alexa Developer Console and for SSL certificate type select:

> My development endpoint is a sub-domain of a domain that has a wildcard certificate from a certificate authority

Click Save Endpoints.

#### Email

In `Event.py`, set `calenderId` to the gmail you'd like to use to create your event.

You are now all set.

### Running

In PyCharm, run `PartyBuddy.py`. If this gives you an error, running it again should redirect you to the Google sign in page in your browser where you can sign in to the same gmail you used before for authorization.

Now click Test at the top of the Alexa Developer Console and you can start interacting with the skill. For example, type in (or click and hold the microphone and say) `ask party buddy to organize a party` to start creating your party on Google Calendar!

## Built With

* [Flask-Ask](https://github.com/johnwheeler/flask-ask) - The Flask extension for Alexa skills development
* [ngrok](https://ngrok.com/) - For a local server
* [Calendar API](https://developers.google.com/calendar/) - Google Calendar API
* [ASK](https://developer.amazon.com/alexa-skills-kit) - Alexa Skills Kit

## Authors

Team Sundae (Katarzyna Koprowska, Miglė Šiaučiulytė and Yu-Jo Tseng)

## Acknowledgments

Huge thanks to our mentor Alistair Smith for helping us with the project.
