from flask import Flask
from flask_ask import Ask, delegate, statement, elicit_slot
import random
import Event

app = Flask(__name__)
ask = Ask(app, '/')


contacts = {'migle': 'migle19@gmail.com', 'kasia': 'katarzyna.joanna.koprowska@gmail.com', 'yujo': 'zoey5538@gmail.com'}
partylist = {'yujo': 'zoey5538@gmail.com'}
themeNumber = 20

with open('PartyThemes', encoding='utf8') as p:
    themes = p.readlines()
with open('PartyThemesDescriptions', encoding='utf8') as d:
    themesDescriptions = d.readlines()
with open('PartyPlaylists', encoding='utf8') as s:
    playlists = s.readlines()
with open('Cocktails', encoding='utf8') as c:
    cocktails=c.readlines()
with open('CocktailsRecipes', encoding='utf8') as r:
    cocktailsRecipes=r.readlines()


# todo: date might be in the past
@ask.intent('OrganizeParty')
def organize_party(date, time, location):
    if date is None or time is None or location is None:
        return delegate()

    Event.create_event(location, date, time)

    print(date)
    print(time)
    print(location)
    return statement(
            'Organizing a party on ' + date + ' at ' + time + ' at ' + location)


# todo: add last name
# add people from our contact list to party list
@ask.intent('Invite')
def add_person(name):
    name = name.lower()
    if name in partylist:
        return statement(name + ' is already in your party list.')
    if name in contacts:
        partylist[name] = contacts[name]
        Event.update_event_invitees(name)
        return statement('Added ' + name + ' to the party list.')
    return statement(name + ' is not in your contact list.')


@ask.intent('PeopleInvited')
def people_invited():
    return statement('You have invited ' + ', '.join(partylist))


# if not invited, want invited?
@ask.intent('IsInvited')
def is_invited(name):
    name = name.lower()
    if name in partylist:
        return statement(name + ' is invited.')
    if name in contacts:
        return statement(name + ' is not invited.')
    return statement(name + ' is not in your contact list.')


# todo: theme description
@ask.intent('SuggestPartyTheme')
def suggest_theme(yes_no):
    global themeNumber
    if yes_no is None:
        themeNumber = random.randint(0, len(themes) - 1)
        return elicit_slot('yes_no', '<speak><s>How about ' + themes[themeNumber] + '?</s> Would you like to use this theme for your party?</speak>')
    if yes_no == 'yes':
        Event.update_event_description(themeNumber)
        return statement('The theme has been added to your calendar event.')
    else:
        themeNumber = 20
        return statement('<speak><emphasis level="strong">Okay.</emphasis></speak>')


@ask.intent('DescribePartyTheme')
def describe_theme():
    return statement(themesDescriptions[themeNumber])

@ask.intent('SuggestCocktail')
def suggest_cocktail():
    global cocktailsNumber
    cocktailsNumber = random.randint(0, len(cocktails) - 1)
    return statement( 'I believe you would like ' + cocktails[cocktailsNumber])


@ask.intent('CocktailRecipe')
def give_recipe():
    return statement(cocktailsRecipes[cocktailsNumber])


@ask.intent('PeopleComing')
def people_coming():
    emails = Event.get_attendees_status()
    names = map(lambda email: getKeyByValue(email, contacts), emails)
    print(names)
    return statement(', '.join(names) + ' are coming')


def getKeyByValue(value, dict):
    for k, v in dict.items():
        if v == value:
            return k
    return None


@ask.intent('SuggestPlaylist')
def suggest_playlist():
    if themeNumber < 20:
        return statement('I think the ' + playlists[themeNumber] + ' playlist on Spotify will be best for your theme.')
    return statement('You have not chosen the theme yet.')


if __name__ == '__main__':
    app.run(debug=True)
