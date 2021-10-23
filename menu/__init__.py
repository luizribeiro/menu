import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional, Sequence, Set, Tuple

import config


class MealPlanner(ABC):
    SALT = "sdklfbn"

    def _init_random_seed(self, date: datetime) -> None:
        random.seed(date.strftime(f"%Y%U-{self.SALT}"))

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
    num_cooks: float


@dataclass
class Recipe:
    name: str
    tags: Set[str]
    num_cooks: float

    def fits(self, meal: Meal) -> bool:
        return self.tags.issubset(meal.tags) and meal.num_cooks >= self.num_cooks


class CurrentMealPlanner(MealPlanner):
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

    OVERRIDES: Dict[str, str] = {
        "Sunday Dinner": "Madalena",
        "Monday Dinner": "Pita bread with baharat cauliflower",
        "Tuesday Dinner": "Mushroom Risotto",
    }

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

    def get_menu(self, date: datetime) -> Tuple[Sequence[str], Sequence[str]]:
        self._init_random_seed(date)

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


def get_menu(date: Optional[datetime] = None) -> Tuple[Sequence[str], Sequence[str]]:
    date = datetime.now(config.get_timezone()) if not date else date
    if date < datetime(2021, 10, 24, tzinfo=config.get_timezone()):
        return OldMealPlanner().get_menu(date)
    return CurrentMealPlanner().get_menu(date)
