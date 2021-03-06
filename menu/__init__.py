import random
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, Optional, Sequence, Tuple

import config
from menu.models import Meal
from menu.recipes import get_all_recipes


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
        Meal(
            name="Monday Lunch",
            tags={"lunch"},
            num_cooks=0.5,
            allow_repeat=True,
        ),
        Meal(name="Monday Dinner", tags={"dinner"}, num_cooks=2),
        Meal(
            name="Tuesday Lunch",
            tags={"lunch"},
            num_cooks=0.5,
            allow_repeat=True,
        ),
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
        this_week = datetime.strptime(f"{year} {week}", "%Y %U")
        # this_week points to the first day of the week, so subtracting a day
        # gives us the previous week
        last_week = this_week - timedelta(days=1)
        lunch, dinner = _get_menu_impl(
            int(last_week.strftime("%Y")),
            int(last_week.strftime("%U")),
        )
        return list(lunch) + list(dinner)

    def get_menu(
        self, year: int, week: int
    ) -> Tuple[Sequence[str], Sequence[str]]:
        last_week_recipes = self.get_last_week_recipes(year, week)

        self._init_random_seed(year, week)
        recipes = list(get_all_recipes()).copy()
        all_recipes = recipes.copy()
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
                try:
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
                except StopIteration:
                    # we basically ran out of recipes, just pick whatever
                    # TODO: add test that covers this
                    # TODO: randomize it a bit
                    recipe = next(
                        filter(
                            lambda r: r.fits(meal),
                            all_recipes,
                        )
                    )

            try:
                recipes.remove(recipe)
            except ValueError:
                pass
            (dinner_menu if index % 2 == 1 else lunch_menu).append(recipe)

        return (
            list(map(lambda r: r.name, lunch_menu))[:7],
            list(map(lambda r: r.name, dinner_menu))[:7],
        )


class HardCodedMenuMealPlanner(MealPlanner):
    def get_menu(
        self, year: int, week: int
    ) -> Tuple[Sequence[str], Sequence[str]]:
        menu = [
            ("skip", "skip"),
            ("skip", "skip"),
            ("skip", "skip"),
            ("skip", "skip"),
            ("skip", "skip"),
            ("skip", "skip"),
            ("skip", "skip"),
        ]
        if year == 2021:
            if week == 52:
                menu = [
                    ("skip", "skip"),
                    ("skip", "skip"),
                    ("Savory pancakes", "Roasted veggies + tenderloin"),
                    ("Mediterranean salad", "Stuffed bell peppers"),
                    ("Bagel with egg", "Pizza"),
                    ("Farro salad", "Pasta al Funghi"),
                    ("Quinoa bowls", "Pea soup"),
                ]
            elif week == 51:
                menu = [
                    ("Farro salad", "Carne de Panela"),
                    ("Chickpea salad", "Roasted sweet potatoes"),
                    ("Rice and beans", "Torta salgada"),
                    ("Bagel with egg", "Mushroom Risotto"),
                    ("Mediterranean salad", "Winter vegetable bowls"),
                    ("Wraps", "Kibe"),
                    ("Tortellini soup", "Pierogi"),
                ]
            elif week == 50:
                menu = [
                    ("Shakshuka", "Roasted veggies + tenderloin"),
                    ("Savory pancakes", "Stuffed bell peppers"),
                    ("Ravioli", "Pita bread with baharat cauliflower"),
                    ("Mediterranean salad", "Madalena"),
                    ("Bagel with egg", "Pasta al Funghi"),
                    ("Soylent", "Lentils with rice"),
                    ("Gnocchi with pumpkin", "Tacos"),
                ]
        elif year == 2022:
            if week == 1:
                menu = [
                    ("Wraps", "Bread + cheese + olives"),
                    ("Ravioli", "Mushroom Risotto"),
                    ("Shakshuka", "Tacos"),
                    ("Bagel with egg", "Roasted sweet potatoes"),
                    ("Farro salad", "Lentil dahl"),
                    ("Mediterranean salad", "Gnocchi with pumpkin"),
                    ("Chickpea salad", "Pita bread with baharat cauliflower"),
                ]
            elif week == 5:
                menu = [
                    ("skip", "Bread + cheese + olives"),
                    ("Omelet", "Lentils with rice"),
                    ("Ravioli", "Alfredo Fusilli"),
                    ("Bagel with egg", "Winter vegetable bowls"),
                    ("Soylent", "Pita bread with baharat cauliflower"),
                    ("Farro salad", "Kibe"),
                    ("Rice and beans", "Roasted sweet potatoes"),
                ]
        return (
            [lunch for lunch, _ in menu],
            [dinner for _, dinner in menu],
        )


def _get_menu_impl(
    year: int, week: int
) -> Tuple[Sequence[str], Sequence[str]]:
    if week == 0:
        # for date format %U (week of the year), all days in a new preceding
        # the first sunday year are considered to be in week 0, so we need to
        # change them so they're in the last week of the previous year
        date = datetime.strptime(f"{year-1}-12-31", "%Y-%m-%d")
        return _get_menu_impl(
            int(date.strftime("%Y")),
            int(date.strftime("%U")),
        )
    if year <= 2021 and week <= 52 or year == 2022 and week <= 5:
        return HardCodedMenuMealPlanner().get_menu(year, week)
    return CurrentMealPlanner().get_menu(year, week)


def get_menu(
    date: Optional[datetime] = None,
) -> Tuple[Sequence[str], Sequence[str]]:
    date = datetime.now(config.get_timezone()) if not date else date
    year = int(date.strftime("%Y"))
    week = int(date.strftime("%U"))
    return _get_menu_impl(year, week)
