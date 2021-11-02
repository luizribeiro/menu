from unittest import TestCase

from pyexpect import expect

import constants
from menu.recipes import get_all_recipes, get_recipe


class RecipeTest(TestCase):
    def test_all_recipes(self) -> None:
        recipes = get_all_recipes()
        for recipe in recipes:
            cooklang_recipe = get_recipe(recipe.name)
            expect(cooklang_recipe).different(None)

    def test_all_ingredients_have_colors(self) -> None:
        recipes = get_all_recipes()
        all_ingredients = {
            ingredient.name.lower().strip()
            for recipe in recipes
            for ingredient in get_recipe(recipe.name).ingredients
        }
        expect(all_ingredients - set(constants.COLORS.keys())).to_be_empty()
