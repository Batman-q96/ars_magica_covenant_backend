from typing import Literal, Callable

import pytest

from dateutil import relativedelta

from characters import wound_tracker

from lib import am5_rolls

def botch_roll(*args, **kwargs):
    raise am5_rolls.BotchedRollExcption

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

    baseline_wounds = [# what does the wound tracker look like at baseline
        # field name    baseline value
        ("light_wounds", 0),
        ("medium_wounds", 0),
        ("heavy_wounds", 0),
        ("incapacitated", False),
        ("dead", False),
    ]
    altered_wounds = [# what do we expect to chagne in the wound tracker
        # field_to_check    expected_value  penalty     damage
        ("light_wounds", 1, -1, 5),
        ("medium_wounds", 1, -3, 10),
        ("heavy_wounds", 1, -5, 15),
        ("incapacitated", True, None, 20),
        ("dead", True, None, 25)
    ]
    
    @pytest.fixture
    def wounded_fixture(self, wound_tracker_fixture: wound_tracker.WoundTracker, damage: int):
        wound_tracker_fixture.take_damage(damage)
        return wound_tracker_fixture
    @pytest.mark.parametrize("field_to_check, expected_value, penalty, damage", altered_wounds)
    @pytest.mark.parametrize("baseline_field, baseline_value", baseline_wounds)
    def test_wounding_no_extra_wounds(self,
            wounded_fixture: wound_tracker.WoundTracker,
            field_to_check: str,
            expected_value: int | Literal[True],
            penalty: int | None,
            damage: int,
            baseline_field: str,
            baseline_value: int | Literal[False]):
        if field_to_check == baseline_field:
            pass
        else:
            assert wounded_fixture.model_computed_fields[baseline_field].wrapped_property.fget(wounded_fixture) == baseline_value
    @pytest.mark.parametrize("field_to_check, expected_value, penalty, damage", altered_wounds)
    def test_wounding_correct_wound_added(self,
            wounded_fixture: wound_tracker.WoundTracker,
            field_to_check: str,
            expected_value: int | Literal[True],
            penalty: int | None,
            damage: int
        ):
        assert wounded_fixture.model_computed_fields[field_to_check].wrapped_property.fget(wounded_fixture) == expected_value
    @pytest.mark.parametrize("field_to_check, expected_value, penalty, damage", altered_wounds)
    def test_wounding_correct_penalty(self,
            wounded_fixture: wound_tracker.WoundTracker,
            field_to_check: str,
            expected_value: int | Literal[True],
            penalty: int | None,
            damage: int,
        ):
        assert wounded_fixture.wound_bonus == penalty