from . import Loc as Data

tmp_data: list[Data] = [
    Data("Chapter 0"),
    Data("Chapter 1", rules=["Lvl 4"]),
    Data("Chapter 2", rules=["Lvl 5"]),
    Data("Chapter 3", rules=["Lvl 10"]),
    Data("Chapter 4", rules=["Prim 15", "Lvl 16"], depends=["The Probe-fessional", "BLADE Level Basics"]),
    Data("Chapter 5", rules=["Lvl 20"], depends=["Renewed Will"]),
    Data("Chapter 6", rules=["Noct 20", "Lvl 24"], depends=["A Friend in Need"]),
    Data("Chapter 7", rules=["Obli 25", "Lvl 28"], depends=["Close Comrades"]),
    Data("Chapter 8", rules=["Mira 10", "Lvl 31"], depends=["The Matchmaker"]),
    Data("Chapter 9", rules=["Lvl 34"], depends=["Spy Games"]),
    Data("Chapter 10", rules=["Sylv 15", "Lvl 39"], depends=["Manhunt"]),
    Data("Chapter 11", rules=["Caul 10", "Lvl 45"], depends=["Boot Camp", "Nine Lives"]),
    Data("Chapter 12", rules=["Lvl 50", "Flight Module"], depends=["A Girls Wings"]),
]
