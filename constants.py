from typing import Mapping, Set

DAYS = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]

COLORS: Mapping[str, str] = {
    # these can come from either https://picular.co/
    # or https://alexbeals.com/projects/colorize/
    "amaranth": "#BE9669",
    "apples": "#D1192D",
    "arugula": "#6C7D3F",
    "basil pesto": "#E8EFB6",
    "bay leaves": "#6F6D34",
    "beets": "#D3246D",
    "brussels sprouts": "#84A64D",
    "butter": "#F0CA5D",
    "butternut squash": "#D27E30",
    "canadian bacon": "#EEBEA6",
    "carrots": "#F6700A",
    "chickpeas": "#F2C792",
    "dukkah spice": "#AF8666",
    "egg": "#F3C114",
    "eggs": "#F3C114",
    "farro": "#B38A5F",
    "flour": "#FCF4EC",
    "garlic": "#EDE0D6",
    "gnocchi": "#ECDAAD",
    "green olives": "#A8A60D",
    "green onion": "#E0E7B6",
    "lemon juice": "#F4C710",
    "lemon": "#F4C710",
    "lettuce": "#A0C845",
    "marinara sauce": "#E81721",
    "milk": "#FCFCF7",
    "mozzarella cheese": "#FCEBBE",
    "olive oil": "#E8BB10",
    "onion": "#DFCE9F",
    "oregano": "#214708",
    "pancetta": "#CE3467",
    "parmesan cheese": "#FCD984",
    "parmesan": "#E1C520",
    "parsley": "#6FA921",
    "pepper": "#877D75",
    "pizza dough": "#DCD1BD",
    "sage": "#588470",
    "salt": "#B9B8B7",
    "shredded chicken": "#FCDBB8",
    "tahini": "#FCDCBF",
    "water": "#3C719C",
}

COMMON_INGREDIENTS: Set[str] = {
    "olive oil",
    "pepper",
    "salt",
    "water",
}
