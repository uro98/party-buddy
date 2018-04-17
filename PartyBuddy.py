from datetime import datetime
import requests

from flask import Flask
from flask_ask import Ask, delegate, statement

app = Flask(__name__)
ask = Ask(app, '/')


@ask.intent('OrganizeParty')
def organize_party():
    return statement("Organizing a party.")


if __name__ == '__main__':
    app.run(debug=True)
