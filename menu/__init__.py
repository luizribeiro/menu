import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional, Sequence, Set, Tuple

import config
from utils import cache


class MealPlanner(ABC):
    SALT = "sdklfbn"

    def _init_random_seed(self, year: int, week: int) -> None:
        random.seed(f"{year}{week}-{self.SALT}")

    @abstractmethod
    def get_menu(self, year: int, week: int) -> Tuple[Sequence[str], Sequence[str]]:
        ...


@dataclass
class Meal:
    name: str
    tags: Set[str]
    num_cooks: float


@dataclass
class Recipe:
    name: str
    tags: Set[str]
    num_cooks: float

    def fits(self, meal: Meal) -> bool:
        return self.tags.issubset(meal.tags) and meal.num_cooks >= self.num_cooks


class CurrentMealPlanner(MealPlanner):
    SALT = "bsdfjbhvbchbc"

    PLAN: Sequence[Meal] = [
        Meal(name="Sunday Lunch", tags={"lunch"}, num_cooks=2),
        Meal(name="Sunday Dinner", tags={"dinner"}, num_cooks=2),
        Meal(name="Monday Lunch", tags={"lunch"}, num_cooks=1.5),
        Meal(name="Monday Dinner", tags={"dinner"}, num_cooks=2),
        Meal(name="Tuesday Lunch", tags={"lunch"}, num_cooks=1.5),
        Meal(name="Tuesday Dinner", tags={"dinner"}, num_cooks=2),
        Meal(name="Wednesday Lunch", tags={"lunch", "solo"}, num_cooks=0.5),
        Meal(name="Wednesday Dinner", tags={"dinner"}, num_cooks=2),
        Meal(name="Thursday Lunch", tags={"lunch", "solo"}, num_cooks=0.5),
        Meal(name="Thursday Dinner", tags={"dinner"}, num_cooks=2),
        Meal(name="Friday Lunch", tags={"lunch", "solo"}, num_cooks=0.5),
        Meal(name="Friday Dinner", tags={"dinner"}, num_cooks=2),
        Meal(name="Saturday Lunch", tags={"lunch"}, num_cooks=2),
        Meal(name="Saturday Dinner", tags={"dinner"}, num_cooks=2),
    ]

    OVERRIDES: Dict[str, str] = {}

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
            name="Pita bread with baharat cauliflower", tags={"dinner"}, num_cooks=1.5
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
    ]

    def get_menu(self, year: int, week: int) -> Tuple[Sequence[str], Sequence[str]]:
        self._init_random_seed(year, week)

        recipes = list(self.RECIPES).copy()
        random.shuffle(recipes)

        lunch_menu = []
        dinner_menu = []
        for index, meal in enumerate(self.PLAN):
            if meal.name in self.OVERRIDES.keys():
                recipe = next(
                    filter(lambda r: r.name == self.OVERRIDES[meal.name], recipes)
                )
            else:
                recipe = next(filter(lambda r: r.fits(meal), recipes))
            recipes.remove(recipe)
            (dinner_menu if index % 2 == 1 else lunch_menu).append(recipe)

        return (
            list(map(lambda r: r.name, lunch_menu))[:7],
            list(map(lambda r: r.name, dinner_menu))[:7],
        )


class OldMealPlanner(CurrentMealPlanner):
    SALT = "sdklfbn"

    OVERRIDES: Dict[str, str] = {
        "Sunday Dinner": "Madalena",
        "Monday Dinner": "Pita bread with baharat cauliflower",
        "Tuesday Dinner": "Mushroom Risotto",
    }


@cache.memoize()
def _get_menu_impl(year: int, week: int) -> Tuple[Sequence[str], Sequence[str]]:
    if year < 2021 or week < 44:
        return OldMealPlanner().get_menu(year, week)
    return CurrentMealPlanner().get_menu(year, week)


def get_menu(date: Optional[datetime] = None) -> Tuple[Sequence[str], Sequence[str]]:
    date = datetime.now(config.get_timezone()) if not date else date
    year = int(date.strftime("%Y"))
    week = int(date.strftime("%U"))
    return _get_menu_impl(year, week)
