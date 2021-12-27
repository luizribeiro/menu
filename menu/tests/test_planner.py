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

    @freeze_time(datetime(2021, 12, 19, tzinfo=config.get_timezone()))
    def test_dec_19(self) -> None:
        menu = list(zip(*get_menu(datetime.now(config.get_timezone()))))
        expect(menu).to_equal(
            [
                ("Farro salad", "Carne de Panela"),
                ("Chickpea salad", "Roasted sweet potatoes"),
                ("Rice and beans", "Torta salgada"),
                ("Bagel with egg", "Mushroom Risotto"),
                ("Mediterranean salad", "Winter vegetable bowls"),
                ("Wraps", "Kibe"),
                ("Tortellini soup", "Pierogi"),
            ]
        )

    @freeze_time(datetime(2021, 12, 26, tzinfo=config.get_timezone()))
    def test_dec_26(self) -> None:
        menu = list(zip(*get_menu(datetime.now(config.get_timezone()))))
        expect(menu).to_equal(
            [
                ("skip", "skip"),
                ("skip", "skip"),
                ("Savory pancakes", "Roasted veggies + tenderloin"),
                ("Mediterranean salad", "Stuffed bell peppers"),
                ("Bagel with egg", "Pizza"),
                ("Farro salad", "Pasta al Funghi"),
                ("Quinoa bowls", "Pea soup"),
            ]
        )
