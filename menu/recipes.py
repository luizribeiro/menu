from glob import glob
from pathlib import Path
from typing import Sequence

from cooklang import Recipe as CookLangRecipe

from menu.models import Recipe


def get_all_recipes() -> Sequence[Recipe]:
    files = glob(r"recipes/*.cook")
    cooklang_recipes = []
    for filename in files:
        fd = open(filename, "r")
        recipe_name = Path(filename).stem
        raw_recipe = fd.read()
        fd.close()
        cooklang_recipes.append(
            (recipe_name, CookLangRecipe.parse(raw_recipe))
        )
    all_recipes = [
        Recipe(
            name=name,
            tags=set(recipe.metadata.get("tags", "").split(", ")),
            num_cooks=float((recipe.metadata.get("num_cooks", ""))),
        )
        for name, recipe in cooklang_recipes
    ]
    all_recipes.sort(key=lambda r: r.name)
    return all_recipes


def get_recipe(name: str) -> CookLangRecipe:
    recipe_dir = Path("./recipes/")
    file = Path(f"./recipes/{name}.cook")
    if not file.is_relative_to(recipe_dir):
        raise Exception("Invalid recipe")
    try:
        fd = open(file, "r")
        raw_recipe = fd.read()
        return CookLangRecipe.parse(raw_recipe)
    except BaseException:
        raise Exception("Invalid recipe")
    finally:
        fd.close()
