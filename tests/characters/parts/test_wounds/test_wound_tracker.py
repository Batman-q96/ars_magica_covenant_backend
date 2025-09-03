"""Tests for wounds and wound tracker"""

# pylint: disable=W0212

from typing import Literal, Tuple

import pytest

from characters.parts.wounds import wound_tracker


from lib.time import time

from lib import am5_rolls


def botch_roll(*args, **kwargs):
    """Helper function to simulate a botched roll"""
    raise am5_rolls.BotchedRollExcption(botch_level=0)
