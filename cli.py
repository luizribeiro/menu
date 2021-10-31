import click
import dateparser
from typing import Dict

import constants
from flask import Flask
from menu import get_menu
from menu.recipes import get_recipe
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


@click.command()
@click.argument("when", default="today")
def groceries(when: str) -> None:
    date = dateparser.parse(when)
    lunch_menu, dinner_menu = get_menu(date)
    all_recipes = {
        name: get_recipe(name)
        for name in (list(lunch_menu) + list(dinner_menu))
    }
    shopping_list: Dict[str, int] = {}
    for recipe_name, recipe in all_recipes.items():
        if len(recipe.ingredients) == 0:
            print(
                f"WARNING: recipe {recipe_name} does not have any ingredients"
            )
        for ingredient in recipe.ingredients:
            name = ingredient.name.lower()
            if name not in shopping_list.keys():
                shopping_list[name] = 0
            shopping_list[name] += 1
    for ingredient in sorted(shopping_list.keys()):
        print(f"{ingredient}: {shopping_list[ingredient]}")
