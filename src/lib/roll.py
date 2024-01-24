import random

def roll_standard(modifier: int = 0) -> int:
    return random.randint(1, 10)+modifier

def roll_stress(botch_dice: int = 1, modifier: int = 0) -> int | bool:
    die_roll = random.randint(0, 9)
    if die_roll == 0:
        return botch_roll(botch_dice, modifier)
    elif die_roll == 1:
        return explode_stress()+modifier
    else:
        return die_roll+modifier

def explode_stress():
    die_roll = random.randint(1, 10)
    if die_roll == 1:
        die_roll = explode_stress()
    return 2*die_roll

def botch_roll(botch_dice_num: int, modifier: int) -> bool | int:
    dice_rolls = [random.randint(0, 9) == 0 for i in range(botch_dice_num)]
    if any(dice_rolls):
        return False
    else:
        return modifier
