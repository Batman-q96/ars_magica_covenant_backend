import random

import pytest

from lib import am5_rolls

@pytest.fixture(autouse=True)
def set_seed():
    # DO NOT CHANGE THIS NUMBER FROM 5297992492366785183 OR ALL RNG TESTS WILL BREAK
    TEST_SEED_VALUE = 5297992492366785183
    random.seed(TEST_SEED_VALUE)

def test_standard_roll():
    # generated from running the test with TEST_SEED_VALUE of 5297992492366785183
    expected_roll_results = [2, 4, 9, 8, 4, 8, 5, 9, 4, 8]
    roll_results = [am5_rolls.roll_standard() for i in range(10)]
    assert(roll_results == expected_roll_results)

def test_botch_roll():
    # generated from running the test with TEST_SEED_VALUE of 5297992492366785183
    expected_roll_results = [0, 1, 2, 3, 4, 5, None, 7, 8, None]
    for i, expected_roll_result in zip(range(10), expected_roll_results):
        try:
            roll_result = am5_rolls._botch_roll(i, i)
            assert roll_result == expected_roll_result
        except am5_rolls.BotchedRollExcption:
            assert expected_roll_result is None

def test_explode_dice():
    # generated from running the test with TEST_SEED_VALUE of 5297992492366785183
    expected_roll_results = [4, 8, 18, 16, 8, 16, 10, 18, 8, 16]
    roll_results = [am5_rolls._explode_stress() for i in range(10)]
    assert(roll_results == expected_roll_results)

def test_stress_roll():
    # generated from running the test with TEST_SEED_VALUE of 5297992492366785183
    expected_roll_results = [8, 8, 7, 3, 7, 4, 8, 3, 7, 4, 9, 8, 4, 7, 5, None, 2, 8, 5, 6]
    for i, expected_roll_result in zip(range(10), expected_roll_results):
        try:
            roll_result = am5_rolls.roll_stress(i+1)
            assert roll_result == expected_roll_result
        except am5_rolls.BotchedRollExcption:
            assert expected_roll_result is None