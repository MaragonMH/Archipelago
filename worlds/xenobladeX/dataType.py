from typing import NamedTuple
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Data:
	name: str = ""
	valid: bool = True
	count: int = 1

@dataclass(frozen=True)
class LocData(Data):
	regions: list[str] = field(default_factory=lambda: ['Menu'])

@dataclass
class GroupType:
	prefix: str
	type: int
	offset: int
	length: int
	count: int = 1

class Requirement(NamedTuple):
	name: str
	count: int = 1

class Rule(NamedTuple):
    region: str
    requirements: list[Requirement] = []