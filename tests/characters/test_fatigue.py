"""Tests for the fatigue tracker"""

import datetime

import pydantic
import pytest

from src.characters import fatigue


class TestFatigue:
    """Overall tests for the fatigue tracker"""

    @pytest.fixture
    def fatigue_tracker_fixture(self) -> fatigue.FatigueTracker:
        """Base fixture upon which to run the fatigue tests"""
        return fatigue.FatigueTracker()

    def test_create(self, fatigue_tracker_fixture):
        """Test proper creation of the fatigue tracker fixture"""
        assert fatigue_tracker_fixture

    def test_create_error_negative_short(self):
        """Test that negative short term fatigue levels are impossible"""
        with pytest.raises(pydantic.ValidationError):
            fatigue.FatigueTracker(short_term_levels=-1)

    def test_create_error_negative_long(self):
        """Test that negative long term fatigue levels are impossible"""
        with pytest.raises(pydantic.ValidationError):
            fatigue.FatigueTracker(long_term_levels=-1)

    def test_get_recovery_time_error(
        self, fatigue_tracker_fixture: fatigue.FatigueTracker
    ):
        """Test that a lack of fatigue levels means we error out"""
        with pytest.raises(fatigue.NoFatigueToRecoverError):
            fatigue_tracker_fixture.get_short_term_recovery_time()

    def test_get_recovery_time(self, fatigue_tracker_fixture: fatigue.FatigueTracker):
        """Test that we properly return the recovery time if we have 1 fatigue level"""
        fatigue_tracker_fixture.short_term_levels += 1
        assert (
            fatigue_tracker_fixture.get_short_term_recovery_time()
            == datetime.timedelta(minutes=2)
        )

    def test_get_recovery_time_with_long_term_levels(
        self, fatigue_tracker_fixture: fatigue.FatigueTracker
    ):
        """Test that we properly return the recovery time if we have both short
        and long term fatigue levels"""
        fatigue_tracker_fixture.short_term_levels += 1
        fatigue_tracker_fixture.long_term_levels += 1
        assert (
            fatigue_tracker_fixture.get_short_term_recovery_time()
            == datetime.timedelta(minutes=10)
        )
