"""Grogs are generic characters that may appear once or fewer times"""

from characters.parts import characterstics
from characters.types import base_character


class Grog(base_character.BaseCharacter):
    """The grog implementation"""

    @classmethod
    def generate_fully_random(cls):
        """Generate a completely random grog"""
        cls(
            characteristics=characterstics.Characteristics.generate_fully_random(),
        )
