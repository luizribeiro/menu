import random
from datetime import datetime
from typing import Optional, Sequence, Tuple

import config


lunch = [
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

dinner = [
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

specials = [
    "Esfiha",
    "Curry",
    "Pierogi",
    "Lasagna",
    "Guinness Stew",
    "Lentil shepherd pie",
    "Chickpea marsala",
]


def get_menu(date: Optional[datetime] = None) -> Tuple[Sequence[str], Sequence[str]]:
    SALT = "sdklfbn"
    date = datetime.now(config.get_timezone()) if not date else date
    random.seed(date.strftime(f"%Y%U-{SALT}"))
    lunch_menu = lunch.copy()
    random.shuffle(lunch_menu)
    dinner_menu = dinner.copy()
    random.shuffle(dinner_menu)
    return lunch_menu, dinner_menu
