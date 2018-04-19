from flask import Flask
from flask_ask import Ask, delegate, statement
import random
import Event

app = Flask(__name__)
ask = Ask(app, '/')

contacts = {'migle': 'migle19@gmail.com', 'kasia': 'katarzyna.joanna.koprowska@gmail.com', 'yujo': 'zoey5538@gmail.com'}
partylist = {'kasia': 'katarzyna.joanna.koprowska@gmail.com', 'yujo': 'zoey5538@gmail.com'}
with open('PartyThemes', encoding='utf8') as p:
    themes = p.readlines()
with open('PartyThemesDescriptions', encoding='utf8') as d:
    themesDescriptions = d.readlines()
with open('Cocktails', encoding='utf8') as c:
    cocktails=c.readlines()
with open('CocktailsRecipes', encoding='utf8') as r:
    cocktailsRecipes = r.readlines()

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
        Event.update_event(name)
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


@ask.intent('SuggestPartyTheme')
def suggest_theme():
    return statement('How about ' + random.choice(themes) + '?')

@ask.intent('Cocktails')
def suggest_cocktails():
    return statement('I believe you would like ' + random.choice(cocktails))

if __name__ == '__main__':
    app.run(debug=True)
