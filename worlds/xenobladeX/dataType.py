from typing import NamedTuple
from dataclasses import dataclass

class Data(NamedTuple):
	name: str
	valid: bool = True
	count: int = 1

class LocData(NamedTuple):
	name: str
	valid: bool = True
	count: int = 1
	regions: list[str] = ["Menu"]

@dataclass
class GroupType:
	type: int
	count: int = 1
	offset: int = 1

class Requirement(NamedTuple):
	name: str
	count: int = 1

class Rule(NamedTuple):
    region: str
    requirements: list[Requirement] = []