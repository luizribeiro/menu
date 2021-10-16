import random
from datetime import datetime, timedelta
from typing import Dict, Optional, Sequence, Tuple
from zoneinfo import ZoneInfo

from flask import Flask, render_template

import config
import constants

app = Flask(__name__)


lunch = [
    "Shakshuka",
    "Farro salad",
    "Bagel with egg",
    "Rice and beans",
    "Ravioli",
    "Mediterranean salad",
    "Quinoa bowls",
    "Soylent",
    "Gnocchi with pumpkin",
    "Chickpea salad",
    "Omelet",
]

dinner = [
    "Lentils with rice",
    "Tacos",
    "Kibe",
    "Pasta al Funghi",
    "Mushroom Risotto",
    "Burgers",
    "Stuffed bell peppers",
    "Pita bread with baharat cauliflower",
    "Tortellini soup",
    "Pizza",
    "Pea soup",
    "Madalena",
    "Roasted sweet potatoes",
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


def get_menu(date: Optional[datetime] = None) -> Tuple[Sequence[str], Sequence[str]]:
    SALT = "sdklfbn"
    date = datetime.now(config.get_timezone()) if not date else date
    random.seed(date.strftime(f"%Y%U-{SALT}"))
    lunch_menu = lunch.copy()
    random.shuffle(lunch_menu)
    dinner_menu = dinner.copy()
    random.shuffle(dinner_menu)
    return lunch_menu, dinner_menu


def get_day_of_the_week() -> int:
    return constants.DAYS.index(datetime.now(config.get_timezone()).strftime("%A"))


@app.route("/")
def index() -> str:
    lunch_menu, dinner_menu = get_menu()
    current_day = get_day_of_the_week()
    content = "<ul>"
    for i, day in enumerate(constants.DAYS):
        if i < current_day:
            continue
        klass = "today" if i == current_day else "future"
        content += f'<li class="{klass}"><b>{day}</b></li>'
        content += '<ul class="{klass}">'
        content += f'<li class="{klass}"><b>Lunch:</b> {lunch_menu[i]}</li>'
        content += f'<li class="{klass}"><b>Dinner:</b> {dinner_menu[i]}</li>'
        content += "</ul>"
    content += "</ul>"

    return render_template("index.html.jinja", content=content)


@app.route("/next_week")
def next_week() -> str:
    date = datetime.now(config.get_timezone()) + timedelta(weeks=+1)
    lunch_menu, dinner_menu = get_menu(date)
    content = "<ul>"
    for i, day in enumerate(constants.DAYS):
        content += f"<li><b>{day}</b></li>"
        content += "<ul>"
        content += f"<li><b>Lunch:</b> {lunch_menu[i]}</li>"
        content += f"<li><b>Dinner:</b> {dinner_menu[i]}</li>"
        content += "</ul>"
    content += "</ul>"

    return render_template("index.html.jinja", content=content)


@app.route("/api/today")
def api_today() -> Dict[str, object]:
    lunch_menu, dinner_menu = get_menu()
    day_of_the_week = get_day_of_the_week()
    return {
        "today": {
            "lunch": lunch_menu[day_of_the_week],
            "dinner": dinner_menu[day_of_the_week],
        }
    }
