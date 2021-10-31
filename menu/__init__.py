import random
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Optional, Sequence, Tuple

import config
from menu.models import Meal
from menu.recipes import get_all_recipes
from utils import cache


class MealPlanner(ABC):
    SALT = "sdklfbn"

    def _init_random_seed(self, year: int, week: int) -> None:
        random.seed(f"{year}{week}-{self.SALT}")

    @abstractmethod
    def get_menu(
        self, year: int, week: int
    ) -> Tuple[Sequence[str], Sequence[str]]:
        ...


class CurrentMealPlanner(MealPlanner):
    SALT = "bsdfjbhvbchbc"

    PLAN: Sequence[Meal] = [
        Meal(name="Sunday Lunch", tags={"lunch"}, num_cooks=2),
        Meal(name="Sunday Dinner", tags={"dinner"}, num_cooks=2),
        Meal(name="Monday Lunch", tags={"lunch"}, num_cooks=1.5),
        Meal(name="Monday Dinner", tags={"dinner"}, num_cooks=2),
        Meal(name="Tuesday Lunch", tags={"lunch"}, num_cooks=1.5),
        Meal(name="Tuesday Dinner", tags={"dinner"}, num_cooks=2),
        Meal(
            name="Wednesday Lunch",
            tags={"lunch", "solo"},
            num_cooks=0.5,
            allow_repeat=True,
        ),
        Meal(name="Wednesday Dinner", tags={"dinner"}, num_cooks=2),
        Meal(
            name="Thursday Lunch",
            tags={"lunch", "solo"},
            num_cooks=0.5,
            allow_repeat=True,
        ),
        Meal(name="Thursday Dinner", tags={"dinner"}, num_cooks=2),
        Meal(
            name="Friday Lunch",
            tags={"lunch", "solo"},
            num_cooks=0.5,
            allow_repeat=True,
        ),
        Meal(name="Friday Dinner", tags={"dinner"}, num_cooks=2),
        Meal(name="Saturday Lunch", tags={"lunch"}, num_cooks=2),
        Meal(name="Saturday Dinner", tags={"dinner"}, num_cooks=2),
    ]

    OVERRIDES: Dict[str, str] = {}

    def get_last_week_recipes(self, year: int, week: int) -> Sequence[str]:
        # FIXME: fix what happens over new years
        lunch, dinner = _get_menu_impl(year, week - 1)
        return lunch + dinner

    def get_menu(
        self, year: int, week: int
    ) -> Tuple[Sequence[str], Sequence[str]]:
        last_week_recipes = self.get_last_week_recipes(year, week)

        self._init_random_seed(year, week)
        recipes = list(get_all_recipes()).copy()
        random.shuffle(recipes)

        lunch_menu = []
        dinner_menu = []
        for index, meal in enumerate(self.PLAN):
            if meal.name in self.OVERRIDES.keys():
                recipe = next(
                    filter(
                        lambda r: r.name == self.OVERRIDES[meal.name], recipes
                    )
                )
            else:
                recipe = next(
                    filter(
                        lambda r: r.fits(meal)
                        and (
                            meal.allow_repeat
                            or r.name not in last_week_recipes
                        ),
                        recipes,
                    )
                )
            recipes.remove(recipe)
            (dinner_menu if index % 2 == 1 else lunch_menu).append(recipe)

        return (
            list(map(lambda r: r.name, lunch_menu))[:7],
            list(map(lambda r: r.name, dinner_menu))[:7],
        )


class VeryFirstMenuMealPlanner(MealPlanner):
    def get_menu(
        self, year: int, week: int
    ) -> Tuple[Sequence[str], Sequence[str]]:
        menu = [
            ("Gnocchi with pumpkin", "Winter vegetable bowls"),
            ("Savory pancakes", "Pizza"),
            ("Farro salad", "Kibe"),
            ("Soylent", "Lentils with rice"),
            ("Bagel with egg", "Roasted veggies + tenderloin"),
            ("Mediterranean salad", "Roasted sweet potatoes"),
            ("Quinoa bowls", "Tacos"),
        ]
        return (
            [lunch for lunch, _ in menu],
            [dinner for _, dinner in menu],
        )


@cache.memoize()
def _get_menu_impl(
    year: int, week: int
) -> Tuple[Sequence[str], Sequence[str]]:
    if year < 2021 or week < 45:
        return VeryFirstMenuMealPlanner().get_menu(year, week)
    return CurrentMealPlanner().get_menu(year, week)


def get_menu(
    date: Optional[datetime] = None,
) -> Tuple[Sequence[str], Sequence[str]]:
    date = datetime.now(config.get_timezone()) if not date else date
    year = int(date.strftime("%Y"))
    week = int(date.strftime("%U"))
    return _get_menu_impl(year, week)
