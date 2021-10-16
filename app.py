import random
from datetime import datetime, timedelta
from typing import Optional, Sequence, Tuple
from zoneinfo import ZoneInfo

from flask import Flask, render_template

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


def get_menu(date: Optional[datetime] = None) -> Tuple[Sequence[str], Sequence[str]]:
    SALT = "sdklfbn"
    date = datetime.now(TIMEZONE) if not date else date
    random.seed(date.strftime(f"%Y%U-{SALT}"))
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
    current_day = get_day_of_the_week()
    content = "<ul>"
    for i, day in enumerate(DAYS):
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
def next_week():
    date = datetime.now(TIMEZONE) + timedelta(weeks=+1)
    lunch_menu, dinner_menu = get_menu(date)
    content = "<ul>"
    for i, day in enumerate(DAYS):
        content += f"<li><b>{day}</b></li>"
        content += "<ul>"
        content += f"<li><b>Lunch:</b> {lunch_menu[i]}</li>"
        content += f"<li><b>Dinner:</b> {dinner_menu[i]}</li>"
        content += "</ul>"
    content += "</ul>"

    return render_template("index.html.jinja", content=content)


@app.route("/api/today")
def api_today():
    lunch_menu, dinner_menu = get_menu()
    day_of_the_week = get_day_of_the_week()
    return {
        "today": {
            "lunch": lunch_menu[day_of_the_week],
            "dinner": dinner_menu[day_of_the_week],
        }
    }
