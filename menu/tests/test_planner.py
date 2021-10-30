from datetime import datetime
from unittest import TestCase

from flask import Flask
from freezegun import freeze_time
from pyexpect import expect

import config
from menu import get_menu
from utils import cache


app = Flask(__name__)
cache.config = {"CACHE_TYPE": "simple"}
cache.init_app(app)


class MealPlannerTest(TestCase):
    @freeze_time(datetime(2021, 10, 30, tzinfo=config.get_timezone()))
    def test_old_menu(self) -> None:
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

    @freeze_time(datetime(2021, 11, 1, tzinfo=config.get_timezone()))
    def test_menu(self) -> None:
        menu = list(zip(*get_menu(datetime.now(config.get_timezone()))))
        expect(menu).to_equal(
            [
                ("Gnocchi with pumpkin", "Winter vegetable bowls"),
                ("Savory pancakes", "Pizza"),
                ("Farro salad", "Kibe"),
                ("Soylent", "Lentils with rice"),
                ("Bagel with egg", "Roasted veggies + tenderloin"),
                ("Mediterranean salad", "Roasted sweet potatoes"),
                ("Quinoa bowls", "Tacos"),
            ]
        )
