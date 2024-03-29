"""Library functions for Ars Magica dice rolls"""

import random


def roll_standard(modifier: int = 0) -> int:
    """Standard dice roll"""
    return random.randint(1, 10) + modifier


def roll_stress(botch_dice: int = 1, modifier: int = 0) -> int:
    """Stress roll with exploding 1s and botch potential on 0"""
    die_roll = random.randint(0, 9)
    if die_roll == 0:
        return _botch_roll(botch_dice, modifier)
    elif die_roll == 1:
        return _explode_stress() + modifier
    else:
        return die_roll + modifier


def _explode_stress():
    die_roll = random.randint(1, 10)
    if die_roll == 1:
        die_roll = _explode_stress()
    return 2 * die_roll


def _botch_roll(botch_dice_num: int, modifier: int) -> int:
    dice_rolls = [random.randint(0, 9) == 0 for i in range(botch_dice_num)]
    if any(dice_rolls):
        raise BotchedRollExcption(botch_level=sum(dice_rolls))
    else:
        return modifier


class BotchedRollExcption(Exception):
    """Exception raised when a stress roll botches"""

    def __init__(
        self,
        *args: object,
        botch_level: int,
    ) -> None:
        super().__init__(*args)
        self.botch_level = botch_level
