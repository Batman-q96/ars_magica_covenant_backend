"""Characterstics are numerical stats describing ars magica characters see ArM5(18)"""

from typing import Self, Generator
import random
import pydantic

_STAT_COSTS = {-3: -6, -2: -3, -1: -1, 0: 0, 1: 1, 2: 3, 3: 6}


class ExtremeCharactersticsError(Exception):
    """Exception raised when characterstics are out of expected bounds"""


class Characteristics(pydantic.BaseModel):
    """Base container class for the main 8 characterstics"""

    strength: int = 0
    stamina: int = 0
    quickness: int = 0
    dexterity: int = 0
    intelligence: int = 0
    perception: int = 0
    presence: int = 0
    communication: int = 0

    def __add__(self, add_val: int) -> Self:
        results_dict = {}
        for char_name, value in self:
            results_dict[char_name] = value + add_val

        return self.__class__(**results_dict)

    def __sub__(self, sub_val: int) -> Self:
        results_dict = {}
        for char_name, value in self:
            results_dict[char_name] = value - sub_val

        return self.__class__(**results_dict)

    @classmethod
    def iter_char_names(cls) -> Generator[str, None, None]:
        """Iterate to get just the names of the characterstics"""
        yield "strength"
        yield "stamina"
        yield "quickness"
        yield "dexterity"
        yield "intelligence"
        yield "perception"
        yield "presence"
        yield "communication"

    def __iter__(self) -> Generator[tuple[str, int], None, None]:
        yield "strength", self.strength
        yield "stamina", self.stamina
        yield "quickness", self.quickness
        yield "dexterity", self.dexterity
        yield "intelligence", self.intelligence
        yield "perception", self.perception
        yield "presence", self.presence
        yield "communication", self.communication

    @classmethod
    def generate_fully_random(cls, rand_min: int = -3, rand_max: int = 3) -> Self:
        """Generate a fully random set of stats"""
        return cls(
            **{
                characteristic: random.randint(rand_min, rand_max)
                for characteristic in cls.iter_char_names()
            }
        )

    def get_characterstics_point_cost(self) -> int:
        """Determine the cost of these characterstics as if they were made in character creation"""

        running_total = 0
        try:
            for _, value in self:
                running_total += _STAT_COSTS[value]
            return running_total
        except KeyError as exc:
            raise ExtremeCharactersticsError from exc

    def is_valid_starting_characterstics(self, max_cost: int = 7) -> bool:
        """Check if the total cost of these characterstics is below the max"""
        try:
            return self.get_characterstics_point_cost() <= max_cost
        except ExtremeCharactersticsError:
            return False

    def is_valid_starting_characterstics_and_fully_spent(
        self, max_cost: int = 7
    ) -> bool:
        """Check if the total cost of these characterstics is exactly at the max"""
        try:
            return self.get_characterstics_point_cost() == max_cost
        except ExtremeCharactersticsError:
            return False
