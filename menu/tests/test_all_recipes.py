from unittest import TestCase

from pyexpect import expect

from menu.recipes import get_all_recipes, get_recipe


class RecipeTest(TestCase):
    def test_all_recipes(self) -> None:
        recipes = get_all_recipes()
        for recipe in recipes:
            cooklang_recipe = get_recipe(recipe.name)
            expect(cooklang_recipe).not_.to_be_none()
