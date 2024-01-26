import pytest

import datetime
from dateutil import relativedelta

from characters import wound_tracker

class TestWounds():
    @pytest.fixture
    def light_wound_fixture(self):
        return wound_tracker.LightWound()
    @pytest.fixture
    def medium_wound_fixture(self):
        return wound_tracker.MediumWound()
    @pytest.fixture
    def heavy_wound_fixture(self):
        return wound_tracker.HeavyWound()
    @pytest.fixture
    def incapacitating_wound_fixture(self):
        return wound_tracker.IncapacitatingWound()
    @pytest.fixture
    def deadly_wound_fixture(self):
        return wound_tracker.DeadlyWound()
    
    def test_light_wound_period(self, light_wound_fixture: wound_tracker.LightWound):
        assert light_wound_fixture.recovery_period == relativedelta.relativedelta(weeks=1)
    def test_light_wound_bonus(self, light_wound_fixture: wound_tracker.LightWound):
        assert light_wound_fixture.bonus == -1
    
    def test_medium_wound_period(self, medium_wound_fixture: wound_tracker.MediumWound):
        assert medium_wound_fixture.recovery_period == relativedelta.relativedelta(months=1)
    def test_medium_wound_bonus(self, medium_wound_fixture: wound_tracker.MediumWound):
        assert medium_wound_fixture.bonus == -3
    
    def test_heavy_wound_period(self, heavy_wound_fixture: wound_tracker.HeavyWound):
        assert heavy_wound_fixture.recovery_period == relativedelta.relativedelta(months=3)
    def test_heavy_wound_bonus(self, heavy_wound_fixture: wound_tracker.HeavyWound):
        assert heavy_wound_fixture.bonus == -5
    
    def test_incapacitating_wound_period(self, incapacitating_wound_fixture: wound_tracker.IncapacitatingWound):
        assert incapacitating_wound_fixture.recovery_period == relativedelta.relativedelta(hours=12)
    def test_incapacitating_wound_bonus(self, incapacitating_wound_fixture: wound_tracker.IncapacitatingWound):
        assert incapacitating_wound_fixture.bonus == None

    def test_deadly_wound_period(self, deadly_wound_fixture: wound_tracker.DeadlyWound):
        assert deadly_wound_fixture.recovery_period == None
    def test_deadly_wound_bonus(self, deadly_wound_fixture: wound_tracker.DeadlyWound):
        assert deadly_wound_fixture.bonus == None
    def test_deadly_wound_recovery_bonus(self, deadly_wound_fixture: wound_tracker.DeadlyWound):
        assert deadly_wound_fixture.recovery_bonus == None

class TestWoundTracker():
    @pytest.fixture
    def wound_tracker_fixture(self) -> wound_tracker.WoundTracker:
        return wound_tracker.WoundTracker(size=0)
    
    @pytest.fixture
    def lightly_wounded_fixture(self, wound_tracker_fixture: wound_tracker.WoundTracker):
        wound_tracker_fixture.take_damage(5)
        return wound_tracker_fixture
    def test_light_wounding(self, lightly_wounded_fixture: wound_tracker.WoundTracker):
        assert len(lightly_wounded_fixture._light_wounds) == 1
    def test_light_wounding_penalty(self, lightly_wounded_fixture: wound_tracker.WoundTracker):
        assert lightly_wounded_fixture.wound_bonus == -1
    @pytest.fixture
    def light_wounding_recovery_bad_fixture(self, lightly_wounded_fixture: wound_tracker.WoundTracker):
        lightly_wounded_fixture.recover_all_light_wounds(0, 0)
        return lightly_wounded_fixture
    def test_light_wound_bad_recovery(self, light_wounding_recovery_bad_fixture: wound_tracker.WoundTracker):
        light_wounding_recovery_bad_fixture.
    
    @pytest.fixture
    def medium_wounded_fixture(self, wound_tracker_fixture: wound_tracker.WoundTracker):
        wound_tracker_fixture.take_damage(10)
        return wound_tracker_fixture
    def test_medium_wounding(self, medium_wounded_fixture: wound_tracker.WoundTracker):
        assert len(medium_wounded_fixture._medium_wounds) == 1
    def test_medium_wounding_penalty(self, medium_wounded_fixture: wound_tracker.WoundTracker):
        assert medium_wounded_fixture.wound_bonus == -3
    
    @pytest.fixture
    def heavily_wounded_fixture(self, wound_tracker_fixture: wound_tracker.WoundTracker):
        wound_tracker_fixture.take_damage(15)
        return wound_tracker_fixture
    def test_heavy_wounding(self, heavily_wounded_fixture: wound_tracker.WoundTracker):
        assert len(heavily_wounded_fixture._heavy_wounds) == 1
    def test_heavy_wounding_penalty(self, heavily_wounded_fixture: wound_tracker.WoundTracker):
        assert heavily_wounded_fixture.wound_bonus == -5

    @pytest.fixture
    def incapacitating_wounded_fixture(self, wound_tracker_fixture: wound_tracker.WoundTracker):
        wound_tracker_fixture.take_damage(20)
        return wound_tracker_fixture
    def test_incapacitating_wounding(self, incapacitating_wounded_fixture: wound_tracker.WoundTracker):
        assert incapacitating_wounded_fixture.incapacitated == True
    def test_incapacitating_wounding_penalty(self, incapacitating_wounded_fixture: wound_tracker.WoundTracker):
        assert incapacitating_wounded_fixture.wound_bonus == None
    
    @pytest.fixture
    def deadly_wounded_fixture(self, wound_tracker_fixture: wound_tracker.WoundTracker):
        wound_tracker_fixture.take_damage(25)
        return wound_tracker_fixture
    def test_deadly_wounding(self, deadly_wounded_fixture: wound_tracker.WoundTracker):
        assert deadly_wounded_fixture.dead == True
    def test_deadly_wounding_penalty(self, deadly_wounded_fixture: wound_tracker.WoundTracker):
        assert deadly_wounded_fixture.wound_bonus == None