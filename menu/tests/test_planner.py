from datetime import datetime
from unittest import TestCase

from freezegun import freeze_time
from pyexpect import expect

import config
from menu import get_menu


class MealPlannerTest(TestCase):
    @freeze_time("2021-10-23")
    def test_old_menu(self) -> None:
        menu = list(zip(*get_menu(datetime.now(config.get_timezone()))))
        expect(menu).to_equal(
            [
                ("Omelet", "Kibe"),
                ("Chickpea salad", "Pizza"),
                ("Ravioli", "Madalena"),
                ("Mediterranean salad", "Burgers"),
                ("Farro salad", "Pasta al Funghi"),
                ("Soylent", "Pita bread with baharat cauliflower"),
                ("Shakshuka", "Stuffed bell peppers"),
            ]
        )

    @freeze_time("2021-10-24")
    def test_menu(self) -> None:
        menu = list(zip(*get_menu(datetime.now(config.get_timezone()))))
        expect(menu).to_equal(
            [
                ("Shakshuka", "Madalena"),
                ("Bagel with egg", "Pita bread with baharat cauliflower"),
                ("Rice and beans", "Mushroom Risotto"),
                ("Soylent", "Roasted sweet potatoes"),
                ("Mediterranean salad", "Kibe"),
                ("Farro salad", "Tortellini soup"),
                ("Omelet", "Pasta al Funghi"),
            ]
        )
