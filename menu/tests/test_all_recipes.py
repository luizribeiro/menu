from datetime import datetime
from unittest import TestCase

from flask import Flask
from freezegun import freeze_time
from pyexpect import expect

import config
from menu import get_menu
from menu.recipes import get_all_recipes, get_recipe
from utils import cache


class RecipeTest(TestCase):
    def test_all_recipes(self) -> None:
        recipes = get_all_recipes()
        for recipe in recipes:
            cooklang_recipe = get_recipe(recipe.name)
            expect(cooklang_recipe).not_.to_be_none()
