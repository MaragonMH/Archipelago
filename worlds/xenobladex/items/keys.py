from ..Items import Itm as Data

# flake8: noqa
other_data: list[Data] = [
Data("Victory", count=0),
Data("Filler", count=0),
]

keys_data:list[Data] = [
Data("Skell License"),
Data("Flight Module"),
Data("Overdrive"),
Data("FNet"),
Data("Blade License"),
Data("Death", count=0),
Data("Kill Enemy", count=0),
*other_data,
]
