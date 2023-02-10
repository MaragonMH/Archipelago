from ..dataType import Requirement as Req, Rule 

doll_regions = [
Rule("Menu"),
Rule("Skell License",[Req("Skell License")]),
Rule("Flight Module",[Req("Flight Module")]),
]

fnet_regions = [
Rule("Menu"),
Rule("FNet", [Req("FNet")]),
]