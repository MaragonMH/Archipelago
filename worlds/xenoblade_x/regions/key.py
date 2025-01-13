from ..Regions import Requirement as Req, Rule 

doll_regions = [
Rule("Menu"),
Rule("Skell License",{Req("KEY: Skell License")}),
Rule("Flight Module",{Req("KEY: Flight Module")}),
]

fnet_regions = [
Rule("Menu"),
Rule("FNet", {Req("KEY: FNet")}),
]