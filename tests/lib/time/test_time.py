import pytest
from lib.time import time
from lib.time.arm5_relative_delta import Arm5RelativeDelta


def test_season_duration():
    assert isinstance(time.SEASON, Arm5RelativeDelta)
    assert time.SEASON.seasons == 1
    assert time.SEASON.months == 3


def test_month_duration():
    assert isinstance(time.MONTH, Arm5RelativeDelta)
    assert time.MONTH.months == 1
    assert time.MONTH.seasons == 0


def test_moon_duration():
    assert isinstance(time.MOON, Arm5RelativeDelta)
    assert time.MOON.months == 1


def test_week_duration():
    assert isinstance(time.WEEK, Arm5RelativeDelta)
    assert time.WEEK.weeks == 1


def test_day_duration():
    assert isinstance(time.DAY, Arm5RelativeDelta)
    assert time.DAY.days == 1


def test_sun_duration():
    assert isinstance(time.SUN, Arm5RelativeDelta)
    assert time.SUN.hours == 12


def test_hour_duration():
    assert isinstance(time.HOUR, Arm5RelativeDelta)
    assert time.HOUR.hours == 1


def test_diameter_duration():
    assert isinstance(time.DIAMETER, Arm5RelativeDelta)
    assert time.DIAMETER.minutes == 2


def test_minute_duration():
    assert isinstance(time.MINUTE, Arm5RelativeDelta)
    assert time.MINUTE.minutes == 1


def test_relative_delta_alias():
    assert time.RelativeDelta is Arm5RelativeDelta
