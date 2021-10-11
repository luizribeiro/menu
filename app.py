import random
from datetime import datetime
from typing import Sequence

from flask import Flask

app = Flask(__name__)


lunch = [
    "Farro salad",
    "Mediterranean salad",
    "Bagel with egg",
    "Rice and beans",
    "Gnocchi with pumpkin",
    "Ravioli",
    "Quinoa bowls",
    "Pita bread with baharat cauliflower",
    "Shakshuka",
    "Chickpea salad",
    "Omelet",
]

dinner = [
    "Burgers",
    "Tacos",
    "Stuffed bell peppers",
    "Pasta al Funghi",
    "Mushroom Risotto",
    "Lentils with rice",
    "Roasted sweet potatoes",
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


def get_meal(recipes: Sequence[str]) -> str:
    return random.choice(lunch)


@app.route("/")
def index():
    SALT = "sdklfbn"
    random.seed(datetime.now().strftime(f"%Y%U-{SALT}"))
    lunch_menu = lunch.copy()
    random.shuffle(lunch_menu)
    dinner_menu = dinner.copy()
    random.shuffle(dinner_menu)

    output = """
    <html>
    <head>
        <title>Menu</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap" rel="stylesheet">
        <style>
        body {
            font-family: 'Open Sans', sans-serif;
            font-weight: 400;
            color: #2d3239
        }

        b {
            font-weight: 700;
        }

        html {
            background-color: #eee;
            margin: auto;
        }

        body {
            border: 1px solid #ccc;
            border-top: 0px;
            border-bottom: 0px;
            max-width: max-content;
            margin: auto;
            padding: 1em 4em 1em 2em;
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
        </style>
    </head>
    <body>
    <h1>🍽️ Menu</h1>
    """
    output += "<ul>"
    for i, day in enumerate(DAYS):
        output += f"<li><b>{day}</b></li>"
        output += "<ul>"
        output += f"<li><b>Lunch:</b> {lunch_menu[i]}</li>"
        output += f"<li><b>Dinner:</b> {dinner_menu[i]}</li>"
        output += "</ul>"
    output += "</ul>"
    output += "</body>"
    output += "</html>"

    return output
