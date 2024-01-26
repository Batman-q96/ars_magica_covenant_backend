import datetime

import pydantic
import pytest

from characters import fatigue

class TestFatigue():
    @pytest.fixture
    def fatigue_tracker_fixture(self) -> fatigue.FatigueTracker:
        return fatigue.FatigueTracker()
    
    def test_create(self, fatigue_tracker_fixture):
        assert(fatigue_tracker_fixture)
    
    def test_create_error_negative_short(self):
        with pytest.raises(pydantic.ValidationError):
            fatigue.FatigueTracker(short_term_levels=-1)
    
    def test_create_error_negative_long(self):
        with pytest.raises(pydantic.ValidationError):
            fatigue.FatigueTracker(long_term_levels=-1)

    def test_get_recovery_time_error(self, fatigue_tracker_fixture: fatigue.FatigueTracker):
        with pytest.raises(ValueError):
            fatigue_tracker_fixture.get_short_term_recovery_time()

    def test_get_recovery_time(self, fatigue_tracker_fixture: fatigue.FatigueTracker):
        fatigue_tracker_fixture.short_term_levels += 1
        assert(fatigue_tracker_fixture.get_short_term_recovery_time() == datetime.timedelta(minutes=2))

    def test_get_recovery_time_with_long_term_levels(self, fatigue_tracker_fixture: fatigue.FatigueTracker):
        fatigue_tracker_fixture.short_term_levels += 1
        fatigue_tracker_fixture.long_term_levels += 1
        assert(fatigue_tracker_fixture.get_short_term_recovery_time() == datetime.timedelta(minutes=10))