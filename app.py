import random
from datetime import datetime
from typing import Sequence, Tuple
from zoneinfo import ZoneInfo

from flask import Flask

app = Flask(__name__)


lunch = [
    "Farro salad",
    "Omelet",
    "Bagel with egg",
    "Rice and beans",
    "Gnocchi with pumpkin",
    "Ravioli",
    "Quinoa bowls",
    "Pita bread with baharat cauliflower",
    "Shakshuka",
    "Chickpea salad",
    "Mediterranean salad",
]

dinner = [
    "Lentils with rice",
    "Tacos",
    "Roasted sweet potatoes",
    "Pasta al Funghi",
    "Mushroom Risotto",
    "Burgers",
    "Stuffed bell peppers",
    "Kibe ",
    "Tortellini soup",
    "Pizza",
    "Madalena",
    "Pea soup",
]

specials = [
    "Esfiha",
    "Curry",
    "Pierogi",
    "Lasagna",
    "Guinness Stew",
    "Lentil shepherd pie",
    "Chickpea marsala",
]

DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
TIMEZONE = ZoneInfo("America/Chicago")


def get_menu() -> Tuple[Sequence[str], Sequence[str]]:
    SALT = "sdklfbn"
    random.seed(datetime.now(TIMEZONE).strftime(f"%Y%U-{SALT}"))
    lunch_menu = lunch.copy()
    random.shuffle(lunch_menu)
    dinner_menu = dinner.copy()
    random.shuffle(dinner_menu)
    return lunch_menu, dinner_menu


def get_day_of_the_week() -> int:
    return DAYS.index(datetime.now(TIMEZONE).strftime("%A"))


@app.route("/")
def index():
    lunch_menu, dinner_menu = get_menu()

    output = """
    <html>
    <head>
        <title>Menu</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap" rel="stylesheet">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
        body {
            font-family: 'Open Sans', sans-serif;
            font-weight: 400;
            color: #2d3239;
        }

        b {
            font-weight: 700;
        }

        html {
            background-color: #eee;
            margin: auto;
            padding: 10px;
        }

        body {
            border: 1px solid #ccc;
            block-size: fit-content;
            max-width: max-content;
            margin: auto;
            padding: 1em 2em 1em 2em;
            background-color: #fff;
        }

        h1 {
            text-align: center;
        }

        ul {
            list-style-type: none;
            margin: 0;
            padding: 0;
        }

        body > ul > ul {
            padding-bottom: 2em;
        }

        body > ul > li {
            text-align: center;
            padding: 0.25em;
        }

        .today {
        }

        .future {
            color: #999;
        }
        </style>
    </head>
    <body>
    <h1>🍽️ Menu</h1>
    """
    current_day = get_day_of_the_week()
    output += "<ul>"
    for i, day in enumerate(DAYS):
        if i < current_day:
            continue
        klass = "today" if i == current_day else "future"
        output += f'<li class="{klass}"><b>{day}</b></li>'
        output += '<ul class="{klass}">'
        output += f'<li class="{klass}"><b>Lunch:</b> {lunch_menu[i]}</li>'
        output += f'<li class="{klass}"><b>Dinner:</b> {dinner_menu[i]}</li>'
        output += "</ul>"
    output += "</ul>"
    output += "</body>"
    output += "</html>"

    return output
