import random

import pytest

from src.lib import roll

@pytest.fixture(autouse=True)
def set_seed():
    # DO NOT CHANGE THIS NUMBER FROM 5297992492366785183 OR ALL RNG TESTS WILL BREAK
    TEST_SEED_VALUE = 5297992492366785183
    random.seed(TEST_SEED_VALUE)

def test_standard_roll():
    # generated from running the test with TEST_SEED_VALUE of 5297992492366785183
    expected_roll_results = [2, 4, 9, 8, 4, 8, 5, 9, 4, 8]
    roll_results = [roll.roll_standard() for i in range(10)]
    assert(roll_results == expected_roll_results)

def test_botch_roll():
    # generated from running the test with TEST_SEED_VALUE of 5297992492366785183
    expected_roll_results = [0, 1, 2, 3, 4, 5, False, 7, 8, False]
    roll_results = [roll._botch_roll(i, i) for i in range(10)]
    assert(roll_results == expected_roll_results)

def test_explode_dice():
    # generated from running the test with TEST_SEED_VALUE of 5297992492366785183
    expected_roll_results = [4, 8, 18, 16, 8, 16, 10, 18, 8, 16]
    roll_results = [roll._explode_stress() for i in range(10)]
    assert(roll_results == expected_roll_results)

def test_stress_roll():
    # generated from running the test with TEST_SEED_VALUE of 5297992492366785183
    expected_roll_results = [8, 8, 7, 3, 7, 4, 8, 3, 7, 4, 9, 8, 4, 7, 5, False, 2, 8, 5, 6]
    roll_results = [roll.roll_stress(i+1) for i in range(10, 30)]
    print(roll_results)
    assert(roll_results == expected_roll_results)