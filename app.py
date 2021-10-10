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
    "Quinoa bowls",
    "Ravioli",
    "Gnocchi with pumpkin",
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
    "Pizza",
    "Roasted sweet potatoes",
    "Kibe ",
    "Tortellini soup",
    "Lentils with rice",
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

    output = "<ul>"
    for i, day in enumerate(DAYS):
        output += f"<li><b>{day}</b></li>"
        output += "<ul>"
        output += f"<li><b>Lunch:</b> {lunch_menu[i]}</li>"
        output += f"<li><b>Dinner:</b> {dinner_menu[i]}</li>"
        output += "</ul>"
    output += "</ul>"

    return output
