import re
import colorsys
import random
from fractions import Fraction
from datetime import datetime, timedelta
from typing import Dict, Optional, Sequence
from urllib.parse import quote as urlencode

from flask import Flask, abort, redirect, render_template
from werkzeug.wrappers import Response

import config
import constants
from cooklang import Ingredient
from menu import get_menu
from menu.recipes import get_recipe
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
    content = '<ul class="index">'
    for i, day in enumerate(constants.DAYS):
        if i < current_day:
            continue
        klass = "today" if i == current_day else "future"
        content += f'<li class="{klass}"><b>{day}</b></li>'
        content += '<ul class="{klass} index">'
        content += f'<li class="{klass}"><b>Lunch:</b> <a href="/recipe/{lunch_menu[i]}">{lunch_menu[i]}</a></li>'  # noqa: E501
        content += f'<li class="{klass}"><b>Dinner:</b> <a href="/recipe/{dinner_menu[i]}">{dinner_menu[i]}</a></li>'  # noqa: E501
        content += "</ul>"
    content += "</ul>"

    return render_template("index.html.jinja", content=content)


@app.route("/next_week")
def next_week() -> str:
    date = datetime.now(config.get_timezone()) + timedelta(weeks=+1)
    lunch_menu, dinner_menu = get_menu(date)
    content = '<ul class="index">'
    for i, day in enumerate(constants.DAYS):
        content += f"<li><b>{day}</b></li>"
        content += '<ul class="index">'
        content += f'<li><b>Lunch:</b> <a href="/recipe/{lunch_menu[i]}/">{lunch_menu[i]}</a></li>'  # noqa: E501
        content += f'<li><b>Dinner:</b> <a href="/recipe/{dinner_menu[i]}/">{dinner_menu[i]}</a></li>'  # noqa: E501
        content += "</ul>"
    content += "</ul>"

    return render_template("index.html.jinja", content=content)


def _get_cook_url() -> str:
    lunch_menu, dinner_menu = get_menu()
    day_of_the_week = get_day_of_the_week()
    recipe = urlencode(
        lunch_menu[day_of_the_week]
        if datetime.now().hour <= 15
        else dinner_menu[day_of_the_week]
    )
    return f"https://menu.thepromisedlan.club/recipe/{recipe}/"


@app.route("/api/today")
def api_today() -> Dict[str, object]:
    lunch_menu, dinner_menu = get_menu()
    day_of_the_week = get_day_of_the_week()
    return {
        "today": {
            "lunch": lunch_menu[day_of_the_week],
            "dinner": dinner_menu[day_of_the_week],
            "url": _get_cook_url(),
        }
    }


@app.route("/cook")
def cook() -> Response:
    return redirect(_get_cook_url(), code=302)


class ColorizedIngredient(Ingredient):
    def __init__(self, ingredient: Ingredient) -> None:
        super().__init__(ingredient.name, ingredient.quantity)

    def get_color(self) -> str:
        name = self.name.lower()
        if name in constants.COLORS.keys():
            return constants.COLORS[name.lower()]
        random.seed(name)
        rgb = colorsys.hls_to_rgb(random.random(), 0.45, 1.0)
        return "#" + "".join(f"{int(c * 255):02X}" for c in rgb)

    def render_quantity(self) -> Optional[str]:
        quantity = self.quantity
        if quantity is None:
            return None
        raw_amount = quantity.amount
        if isinstance(raw_amount, Fraction):
            amount = f"{raw_amount.numerator}\u2044{raw_amount.denominator}"
        elif isinstance(raw_amount, float):
            amount = f"{round(raw_amount, 1)}"
        else:
            amount = f"{raw_amount}"
        if quantity.unit:
            return f"{amount} {quantity.unit}"
        return f"{amount}"


def colorize_recipe_step(
    ingredients: Sequence[ColorizedIngredient],
    step: str,
) -> str:
    sorted_ingredients = list(ingredients)
    sorted_ingredients.sort(key=lambda x: len(x.name), reverse=True)
    for ingredient in sorted_ingredients:
        step = re.sub(
            r"(" + ingredient.name + r")(?![^<]*</span>)",
            f"""<span class="ingredient"
                    style="--ingredient-color: {ingredient.get_color()};"
                    >{ingredient.name}</span>""",
            step,
        )
    # render fractions nicely with unicode
    return re.sub(r"([0-9]+)/([0-9]+)", r"\1⁄\2", step)


@app.route("/recipe/<string:name>/")
def recipe(name: str) -> str:
    try:
        recipe = get_recipe(name)
        ingredients = [ColorizedIngredient(i) for i in recipe.ingredients]
        return render_template(
            "recipe.html.jinja",
            name=name,
            ingredients=ingredients,
            steps=recipe.steps,
            colorize_recipe_step=lambda step: colorize_recipe_step(
                ingredients, step
            ),
            is_common_ingredient=lambda x: x.lower()
            in constants.COMMON_INGREDIENTS,
        )
    except BaseException:
        abort(404)
