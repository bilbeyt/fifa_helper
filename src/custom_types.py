"""This module is created for creating custom typings"""
from typing import TypedDict, Tuple, List


class Player(TypedDict):
    """This class is a typeddict type for returning players from db"""
    name: str
    age: int
    nationality: str
    club: str
    photo: str
    overall: int
    value: int
    position: str


PlayerTuple = Tuple[str, int, str, str, int, int, str]
PlayerCreateTuple = Tuple[int, str, int, str, str, str, int, float, str]

class BuilderData(TypedDict):
    """This class is a typeddict type for TeamBuilder data"""
    team: List[Player]
    overall: int
    spent: int
    remaining: int
