import random
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Sequence, Tuple

import config


class MenuResolver(ABC):
    def _init_random_seed(self, date: Optional[datetime]) -> None:
        SALT = "sdklfbn"
        date = datetime.now(config.get_timezone()) if not date else date
        random.seed(date.strftime(f"%Y%U-{SALT}"))

    @abstractmethod
    def get_menu(self, date: Optional[datetime]) -> Tuple[Sequence[str], Sequence[str]]:
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

    def get_menu(self, date: Optional[datetime]) -> Tuple[Sequence[str], Sequence[str]]:
        self._init_random_seed(date)

        lunch_menu = self.LUNCH.copy()
        random.shuffle(lunch_menu)
        dinner_menu = self.DINNER.copy()
        random.shuffle(dinner_menu)

        return lunch_menu, dinner_menu


def get_menu(date: Optional[datetime] = None) -> Tuple[Sequence[str], Sequence[str]]:
    return OldMenuResolver().get_menu(date)
