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
    @freeze_time(datetime(2021, 12, 5, tzinfo=config.get_timezone()))
    def test_dec_11(self) -> None:
        menu = list(zip(*get_menu(datetime.now(config.get_timezone()))))
        expect(menu).to_equal(
            [
                ("Rice and beans", "Stuffed bell peppers"),
                ("Omelet", "Tortellini soup"),
                ("Shakshuka", "Pizza"),
                ("Soylent", "Torta salgada"),
                ("Bagel with egg", "Pea soup"),
                ("Mediterranean salad", "Lentil dahl"),
                ("Chickpea salad", "Mushroom Risotto"),
            ]
        )

    @freeze_time(datetime(2021, 12, 12, tzinfo=config.get_timezone()))
    def test_dec_12(self) -> None:
        menu = list(zip(*get_menu(datetime.now(config.get_timezone()))))
        expect(menu).to_equal(
            [
                ("Shakshuka", "Roasted veggies + tenderloin"),
                ("Savory pancakes", "Stuffed bell peppers"),
                ("Ravioli", "Pita bread with baharat cauliflower"),
                ("Mediterranean salad", "Madalena"),
                ("Bagel with egg", "Pasta al Funghi"),
                ("Soylent", "Lentils with rice"),
                ("Gnocchi with pumpkin", "Tacos"),
            ]
        )
