import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Sequence, Set, Tuple

import config


class MenuResolver(ABC):
    def _init_random_seed(self, date: datetime) -> None:
        SALT = "sdklfbn"
        random.seed(date.strftime(f"%Y%U-{SALT}"))

    @abstractmethod
    def get_menu(self, date: datetime) -> Tuple[Sequence[str], Sequence[str]]:
        ...


class OldMenuResolver(MenuResolver):
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
class Recipe:
    name: str
    tags: Set[str]


class CurrentMenuResolver(MenuResolver):
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

        lunch_menu = list(filter(lambda r: "lunch" in r.tags, self.RECIPES)).copy()
        random.shuffle(lunch_menu)
        dinner_menu = list(filter(lambda r: "dinner" in r.tags, self.RECIPES)).copy()
        random.shuffle(dinner_menu)

        return (
            list(map(lambda r: r.name, lunch_menu))[:7],
            list(map(lambda r: r.name, dinner_menu))[:7],
        )


def get_menu(date: Optional[datetime] = None) -> Tuple[Sequence[str], Sequence[str]]:
    date = datetime.now(config.get_timezone()) if not date else date
    if date < datetime(2021, 10, 24):
        return OldMenuResolver().get_menu(date)
    return CurrentMenuResolver().get_menu(date)
