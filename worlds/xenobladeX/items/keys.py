from ..dataType import Data

other_data:list[Data] = [
Data("Victory", count=0),
Data("Filler", count=0),	
]

keys_data:list[Data] = [
Data("Skell License"),
Data("Flight Module"),
Data("Overdrive"),
Data("FNet"),
*other_data,
]