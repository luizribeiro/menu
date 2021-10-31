from dataclasses import dataclass
from typing import Set


@dataclass
class Meal:
    name: str
    tags: Set[str]
    num_cooks: float
    allow_repeat: bool = False


@dataclass
class Recipe:
    name: str
    tags: Set[str]
    num_cooks: float

    def fits(self, meal: Meal) -> bool:
        return (
            self.tags.issubset(meal.tags) and meal.num_cooks >= self.num_cooks
        )
