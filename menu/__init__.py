import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Sequence, Set, Tuple

import config


class MealPlanner(ABC):
    def _init_random_seed(self, date: datetime) -> None:
        SALT = "sdklfbn"
        random.seed(date.strftime(f"%Y%U-{SALT}"))

    @abstractmethod
    def get_menu(self, date: datetime) -> Tuple[Sequence[str], Sequence[str]]:
        ...


class OldMealPlanner(MealPlanner):
    LUNCH = [
        "Shakshuka",
        "Farro salad",
        "Bagel with egg",
        "Rice and beans",
        "Ravioli",
        "Mediterranean salad",
        "Quinoa bowls",
        "Soylent",
        "Gnocchi with pumpkin",
        "Chickpea salad",
        "Omelet",
    ]

    DINNER = [
        "Lentils with rice",
        "Tacos",
        "Kibe",
        "Pasta al Funghi",
        "Mushroom Risotto",
        "Burgers",
        "Stuffed bell peppers",
        "Pita bread with baharat cauliflower",
        "Tortellini soup",
        "Pizza",
        "Pea soup",
        "Madalena",
        "Roasted sweet potatoes",
    ]

    SPECIALS = [
        "Esfiha",
        "Curry",
        "Pierogi",
        "Lasagna",
        "Guinness Stew",
        "Lentil shepherd pie",
        "Chickpea marsala",
    ]

    def get_menu(self, date: datetime) -> Tuple[Sequence[str], Sequence[str]]:
        self._init_random_seed(date)

        lunch_menu = self.LUNCH.copy()
        random.shuffle(lunch_menu)
        dinner_menu = self.DINNER.copy()
        random.shuffle(dinner_menu)

        return lunch_menu[:7], dinner_menu[:7]


@dataclass
class Meal:
    name: str
    tags: Set[str]


@dataclass
class Recipe:
    name: str
    tags: Set[str]

    def fits(self, meal: Meal) -> bool:
        return meal.tags.issubset(self.tags)


class CurrentMealPlanner(MealPlanner):
    PLAN: Sequence[Meal] = [
        Meal(name="Sunday Lunch", tags={"lunch"}),
        Meal(name="Sunday Dinner", tags={"dinner"}),
        Meal(name="Monday Lunch", tags={"lunch"}),
        Meal(name="Monday Dinner", tags={"dinner"}),
        Meal(name="Tuesday Lunch", tags={"lunch"}),
        Meal(name="Tuesday Dinner", tags={"dinner"}),
        Meal(name="Wednesday Lunch", tags={"lunch"}),
        Meal(name="Wednesday Dinner", tags={"dinner"}),
        Meal(name="Thursday Lunch", tags={"lunch"}),
        Meal(name="Thursday Dinner", tags={"dinner"}),
        Meal(name="Friday Lunch", tags={"lunch"}),
        Meal(name="Friday Dinner", tags={"dinner"}),
        Meal(name="Saturday Lunch", tags={"lunch"}),
        Meal(name="Saturday Dinner", tags={"dinner"}),
    ]

    RECIPES: Sequence[Recipe] = [
        Recipe(name="Shakshuka", tags={"lunch"}),
        Recipe(name="Farro salad", tags={"lunch"}),
        Recipe(name="Bagel with egg", tags={"lunch"}),
        Recipe(name="Rice and beans", tags={"lunch"}),
        Recipe(name="Ravioli", tags={"lunch"}),
        Recipe(name="Mediterranean salad", tags={"lunch"}),
        Recipe(name="Quinoa bowls", tags={"lunch"}),
        Recipe(name="Soylent", tags={"lunch"}),
        Recipe(name="Gnocchi with pumpkin", tags={"lunch"}),
        Recipe(name="Chickpea salad", tags={"lunch"}),
        Recipe(name="Omelet", tags={"lunch"}),
        Recipe(name="Lentils with rice", tags={"dinner"}),
        Recipe(name="Tacos", tags={"dinner"}),
        Recipe(name="Kibe", tags={"dinner"}),
        Recipe(name="Pasta al Funghi", tags={"dinner"}),
        Recipe(name="Mushroom Risotto", tags={"dinner"}),
        Recipe(name="Burgers", tags={"dinner"}),
        Recipe(name="Stuffed bell peppers", tags={"dinner"}),
        Recipe(name="Pita bread with baharat cauliflower", tags={"dinner"}),
        Recipe(name="Tortellini soup", tags={"dinner"}),
        Recipe(name="Pizza", tags={"dinner"}),
        Recipe(name="Pea soup", tags={"dinner"}),
        Recipe(name="Madalena", tags={"dinner"}),
        Recipe(name="Roasted sweet potatoes", tags={"dinner"}),
        Recipe(name="Esfiha", tags={"special"}),
        Recipe(name="Curry", tags={"special"}),
        Recipe(name="Pierogi", tags={"special"}),
        Recipe(name="Lasagna", tags={"special"}),
        Recipe(name="Guinness Stew", tags={"special"}),
        Recipe(name="Lentil shepherd pie", tags={"special"}),
        Recipe(name="Chickpea marsala", tags={"special"}),
    ]

    def get_menu(self, date: datetime) -> Tuple[Sequence[str], Sequence[str]]:
        self._init_random_seed(date)

        recipes = list(self.RECIPES).copy()
        random.shuffle(recipes)

        lunch_menu = []
        dinner_menu = []
        for index, meal in enumerate(self.PLAN):
            recipe = next(filter(lambda r: r.fits(meal), recipes))
            recipes.remove(recipe)
            (dinner_menu if index % 2 == 1 else lunch_menu).append(recipe)

        return (
            list(map(lambda r: r.name, lunch_menu))[:7],
            list(map(lambda r: r.name, dinner_menu))[:7],
        )


def get_menu(date: Optional[datetime] = None) -> Tuple[Sequence[str], Sequence[str]]:
    date = datetime.now(config.get_timezone()) if not date else date
    if date < datetime(2021, 10, 24):
        return OldMealPlanner().get_menu(date)
    return CurrentMealPlanner().get_menu(date)
