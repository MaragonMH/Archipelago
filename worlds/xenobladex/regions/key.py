from typing import List
from ..Regions import Requirement as Req, Rule

# flake8: noqa
doll_regions: List[Rule] = [
Rule("Menu"),
Rule("Blade License", {Req("KEY: Blade License")}),
Rule("Skell License", {Req("KEY: Skell License")}),
Rule("Flight Module", {Req("KEY: Flight Module")}),
]

fnet_regions: List[Rule] = [
Rule("Menu"),
Rule("FNet", {Req("KEY: FNet")}),
]