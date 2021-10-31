import click
import dateparser

import constants
from flask import Flask
from menu import get_menu
from utils import cache


app = Flask(__name__)
cache.init_app(app)


@click.command()
@click.argument("when", default="today")
def menu(when: str) -> None:
    date = dateparser.parse(when)
    lunch_menu, dinner_menu = get_menu(date)
    for i, day in enumerate(constants.DAYS):
        print(f"* {day}")
        print(f"  Lunch: {lunch_menu[i]}")
        print(f"  Dinner: {dinner_menu[i]}")
        if i < 6:
            print()
