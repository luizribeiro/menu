from datetime import datetime
from unittest import TestCase

from freezegun import freeze_time
from pyexpect import expect

import config
from menu import get_menu


class MealPlannerTest(TestCase):
    @freeze_time(datetime(2021, 10, 23, tzinfo=config.get_timezone()))
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

    @freeze_time(datetime(2021, 10, 24, tzinfo=config.get_timezone()))
    def test_menu(self) -> None:
        menu = list(zip(*get_menu(datetime.now(config.get_timezone()))))
        expect(menu).to_equal(
            [
                ("Omelet", "Madalena"),
                ("Rice and beans", "Pita bread with baharat cauliflower"),
                ("Ravioli", "Mushroom Risotto"),
                ("Soylent", "Pea soup"),
                ("Mediterranean salad", "Stuffed bell peppers"),
                ("Bagel with egg", "Pasta al Funghi"),
                ("Shakshuka", "Tortellini soup"),
            ]
        )
