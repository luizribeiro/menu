from datetime import datetime, timedelta
from typing import Dict

from flask import Flask, render_template

import config
import constants
from menu import get_menu

app = Flask(__name__)


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
