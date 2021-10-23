from datetime import datetime
from unittest import TestCase

from freezegun import freeze_time
from pyexpect import expect

from menu import get_menu


class MenuResolverTest(TestCase):
    @freeze_time("2021-10-23")
    def test_old_menu(self) -> None:
        menu = get_menu(datetime.now())
        expect(menu).to_equal(
            (
                [
                    "Omelet",
                    "Chickpea salad",
                    "Ravioli",
                    "Mediterranean salad",
                    "Farro salad",
                    "Soylent",
                    "Shakshuka",
                    "Quinoa bowls",
                    "Gnocchi with pumpkin",
                    "Rice and beans",
                    "Bagel with egg",
                ],
                [
                    "Kibe",
                    "Pizza",
                    "Madalena",
                    "Burgers",
                    "Pasta al Funghi",
                    "Pita bread with baharat cauliflower",
                    "Stuffed bell peppers",
                    "Mushroom Risotto",
                    "Roasted sweet potatoes",
                    "Lentils with rice",
                    "Pea soup",
                    "Tacos",
                    "Tortellini soup",
                ],
            ),
        )
