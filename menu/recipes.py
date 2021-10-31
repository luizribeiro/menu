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
    cooklang_recipes.sort(key=lambda r: int(r[1].metadata.get("index", "0")))
    return [
        Recipe(
            name=name,
            tags=set(recipe.metadata.get("tags", "").split(", ")),
            num_cooks=float((recipe.metadata.get("num_cooks", ""))),
        )
        for name, recipe in cooklang_recipes
    ]
