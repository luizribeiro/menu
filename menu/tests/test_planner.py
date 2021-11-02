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
    @freeze_time(datetime(2021, 10, 31, tzinfo=config.get_timezone()))
    def test_old_menu(self) -> None:
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

    @freeze_time(datetime(2021, 11, 7, tzinfo=config.get_timezone()))
    def test_menu(self) -> None:
        menu = list(zip(*get_menu(datetime.now(config.get_timezone()))))
        expect(menu).to_equal(
            [
                ("Chickpea salad", "Tortellini soup"),
                ("Rice and beans", "Pasta al Funghi"),
                ("Shakshuka", "Stuffed bell peppers"),
                ("Farro salad", "Pea soup"),
                ("Mediterranean salad", "Bread + cheese + olives"),
                ("Soylent", "Lentil dahl"),
                ("Omelet", "Torta salgada"),
            ]
        )
