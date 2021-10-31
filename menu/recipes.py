from typing import Sequence

from menu.models import Recipe


RECIPES: Sequence[Recipe] = [
    Recipe(name="Shakshuka", tags={"lunch"}, num_cooks=1.5),
    Recipe(name="Farro salad", tags={"lunch"}, num_cooks=0.5),
    Recipe(name="Bagel with egg", tags={"lunch"}, num_cooks=0.5),
    Recipe(name="Rice and beans", tags={"lunch"}, num_cooks=1.5),
    Recipe(name="Mediterranean salad", tags={"lunch", "solo"}, num_cooks=0.5),
    Recipe(name="Ravioli", tags={"lunch"}, num_cooks=0.5),
    Recipe(name="Quinoa bowls", tags={"lunch"}, num_cooks=1.5),
    Recipe(name="Soylent", tags={"lunch", "solo"}, num_cooks=0),
    Recipe(name="Gnocchi with pumpkin", tags={"lunch"}, num_cooks=1.5),
    Recipe(name="Chickpea salad", tags={"lunch"}, num_cooks=1.5),
    Recipe(name="Omelet", tags={"lunch"}, num_cooks=1.5),
    Recipe(name="Lentils with rice", tags={"dinner"}, num_cooks=1.5),
    Recipe(name="Tacos", tags={"dinner"}, num_cooks=1.5),
    Recipe(name="Kibe", tags={"dinner"}, num_cooks=1.5),
    Recipe(name="Pasta al Funghi", tags={"dinner"}, num_cooks=1.5),
    Recipe(name="Mushroom Risotto", tags={"dinner"}, num_cooks=0.5),
    Recipe(name="Burgers", tags={"lunch", "dinner", "solo"}, num_cooks=0.5),
    Recipe(name="Stuffed bell peppers", tags={"dinner"}, num_cooks=1.5),
    Recipe(
        name="Pita bread with baharat cauliflower",
        tags={"dinner"},
        num_cooks=1.5,
    ),
    Recipe(name="Tortellini soup", tags={"dinner"}, num_cooks=0.5),
    Recipe(name="Pizza", tags={"dinner"}, num_cooks=1.5),
    Recipe(name="Pea soup", tags={"dinner"}, num_cooks=1.5),
    Recipe(name="Madalena", tags={"dinner"}, num_cooks=1.5),
    Recipe(name="Roasted sweet potatoes", tags={"dinner"}, num_cooks=1.5),
    Recipe(name="Esfiha", tags={"special"}, num_cooks=2),
    Recipe(name="Curry", tags={"special"}, num_cooks=0.5),
    Recipe(name="Pierogi", tags={"special"}, num_cooks=1.5),
    Recipe(name="Lasagna", tags={"special"}, num_cooks=1.5),
    Recipe(name="Guinness Stew", tags={"special"}, num_cooks=2),
    Recipe(name="Lentil shepherd pie", tags={"special"}, num_cooks=2),
    Recipe(name="Chickpea marsala", tags={"special"}, num_cooks=2),
    Recipe(name="Bread + cheese + olives", tags={"dinner"}, num_cooks=0.5),
    Recipe(name="Winter vegetable bowls", tags={"dinner"}, num_cooks=1.5),
    Recipe(name="Pasta primavera", tags={"lunch", "dinner"}, num_cooks=1.5),
    Recipe(name="Lentil dahl", tags={"dinner"}, num_cooks=1.5),
    Recipe(name="Torta salgada", tags={"dinner"}, num_cooks=1.5),
    Recipe(name="Quiche", tags={"special"}, num_cooks=1.5),
    Recipe(
        name="Roasted veggies + tenderloin", tags={"dinner"}, num_cooks=1.5
    ),
    Recipe(name="Savory pancakes", tags={"lunch"}, num_cooks=1.5),
]


def get_all_recipes() -> Sequence[Recipe]:
    return RECIPES
