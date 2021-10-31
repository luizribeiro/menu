from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict

from flask import Flask, abort, render_template

import config
import constants
from cooklang import Recipe
from menu import get_menu
from utils import cache


app = Flask(__name__)
cache.init_app(app)


def get_day_of_the_week() -> int:
    return constants.DAYS.index(
        datetime.now(config.get_timezone()).strftime("%A")
    )


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
        content += f'<li class="{klass}"><b>Lunch:</b> <a href="/recipe/{lunch_menu[i]}">{lunch_menu[i]}</a></li>'
        content += f'<li class="{klass}"><b>Dinner:</b> <a href="/recipe/{dinner_menu[i]}">{dinner_menu[i]}</a></li>'
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
        content += f'<li><b>Lunch:</b> <a href="/recipe/{lunch_menu[i]}/">{lunch_menu[i]}</a></li>'
        content += f'<li><b>Dinner:</b> <a href="/recipe/{dinner_menu[i]}/">{dinner_menu[i]}</a></li>'
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


@app.route("/recipe/<string:name>/")
def recipe(name: str) -> str:
    recipe_dir = Path("./recipes/")
    file = Path(f"./recipes/{name}.cook")
    if not file.is_relative_to(recipe_dir):
        abort(500)
    try:
        fd = open(file, "r")
        raw_recipe = fd.read()
        recipe = Recipe.parse(raw_recipe)
        fd.close()

        return f"""
Recipe: {name}
Ingredients: {recipe.ingredients}
Steps: {recipe.steps}
"""
    except FileNotFoundError:
        abort(404)
