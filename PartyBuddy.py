from flask import Flask
from flask_ask import Ask, delegate, statement, elicit_slot, request
import random
import Event

app = Flask(__name__)
ask = Ask(app, '/')


contacts = {'alistair': 'something@gmail.com', 'anna': 'something@gmail.com', 'yujo': 'something@gmail.com'}
partylist = {}
themeNumber = 20
groceries = []

with open('PartyThemes', encoding='utf8') as p:
    themes = p.readlines()
with open('PartyThemesDescriptions', encoding='utf8') as d:
    themesDescriptions = d.readlines()
with open('PartyPlaylists', encoding='utf8') as s:
    playlists = s.readlines()
with open('Cocktails', encoding='utf8') as c:
    cocktails = c.readlines()
with open('CocktailsRecipes', encoding='utf8') as r:
    cocktailsRecipes = r.readlines()


# todo: date might be in the past
@ask.intent('OrganizeParty')
def organize_party(date, time, location):
    if date is None or time is None or location is None:
        return delegate()

    Event.create_event(location, date, time)
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

    answer = request.intent.slots.yes_no.resolutions.resolutionsPerAuthority[0]['values'][0]['value']['name']
    if answer == 'describe':
        return elicit_slot('yes_no', themesDescriptions[themeNumber] + ' So, would you like to use this theme for your party?')
    if answer == 'yes':
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
    return statement('I believe you would like the ' + cocktails[cocktailsNumber])


@ask.intent('CocktailRecipe')
def give_recipe():
    return statement(cocktailsRecipes[cocktailsNumber] + ' Enjoy.')


@ask.intent('PeopleComing')
def people_coming():
    emails = Event.get_attendees_status()
    names = list(map(lambda email: getKeyByValue(email, contacts), emails))
    if len(names) > 1:
        return statement(', '.join(names) + ' are coming')
    if names:
        return statement(' '.join(names) + ' is coming')
    return statement('Noone has accepted your invitation yet, you loser, hahaha')


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


@ask.intent('WhatToBuy')
def what_to_buy(item, second_item):
    if item in groceries:
        if second_item is None:
            return statement(item + ' is already on your shopping list.')
        if second_item in groceries:
            return statement(item + ' and ' + second_item + ' are already on your shopping list.')
        groceries.append(second_item)
        return statement('I have added ' + second_item + ' to your shopping list, but ' + item + ' is already on your shopping list.')
    if second_item in groceries:
        return statement('I have added '+ item + ' to your shopping list, but ' + second_item + ' is already on your shopping list.')
    groceries.append(item)
    if second_item is None:
        return statement('I have added '+ item + ' to your shopping list.')
    else:
        groceries.append(second_item)
        return statement('I have added ' + item + ' and ' + second_item + ' to your shopping list.')


@ask.intent('GroceryList')
def grocery_list():
    if groceries:
        return statement('Your grocery list contains ' + ', '.join(groceries))
    return statement('Your grocery list is empty.')


#todo: if not, would you like to add it?
@ask.intent('AmIBuying')
def am_i_buying(item):
    if item in groceries:
        return statement('Yes, ' + item + ' is on your shopping list.')
    return statement('No, ' + item + ' is not on your shopping list.')


@ask.intent('RemoveFromGroceryList')
def remove_item(item):
    if item in groceries:
        groceries.remove(item)
        return statement(item + ' was successfully removed.')
    return statement('There is no such item on your shopping list.')


if __name__ == '__main__':
    app.run(debug=True)
