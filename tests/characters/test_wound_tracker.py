from typing import Literal, Callable, Tuple

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
    
    @pytest.fixture
    def healed_light_wound_fixture(self, light_wound_fixture: wound_tracker.LightWound, recovery_result: int):
        light_wound_fixture.heal(recovery_result)
        return light_wound_fixture
    @pytest.mark.parametrize("recovery_result, expected_wound_condition", [
        (wound_tracker.LightWound._STABLE_EASE_FACTOR-1, wound_tracker.WoundStatus.WORSE),
        (wound_tracker.LightWound._STABLE_EASE_FACTOR, wound_tracker.WoundStatus.SAME),
        (wound_tracker.LightWound._RECOVERY_EASE_FACTOR, wound_tracker.WoundStatus.BETTER),
        (3, wound_tracker.WoundStatus.WORSE),
        (4, wound_tracker.WoundStatus.SAME),
        (10, wound_tracker.WoundStatus.BETTER),
    ])
    def test_light_wound_healing(self,
            healed_light_wound_fixture: wound_tracker.LightWound,
            expected_wound_condition: wound_tracker.WoundStatus
        ):
        assert healed_light_wound_fixture.status == expected_wound_condition
    @pytest.mark.parametrize("recovery_result, expected_bonus", [
        (wound_tracker.LightWound._STABLE_EASE_FACTOR, wound_tracker.LightWound._STABLE_RECOVERY_BONUS),
        (wound_tracker.LightWound._STABLE_EASE_FACTOR, 3),
    ])
    def test_light_wound_stable_bonus(self,
            healed_light_wound_fixture: wound_tracker.LightWound,
            expected_bonus: int
        ):
        assert healed_light_wound_fixture.recovery_bonus == expected_bonus
    
    def test_medium_wound_period(self, medium_wound_fixture: wound_tracker.MediumWound):
        assert medium_wound_fixture.recovery_period == relativedelta.relativedelta(months=1)
    def test_medium_wound_bonus(self, medium_wound_fixture: wound_tracker.MediumWound):
        assert medium_wound_fixture.bonus == -3
    
    @pytest.fixture
    def healed_medium_wound_fixture(self, medium_wound_fixture: wound_tracker.MediumWound, recovery_result: int):
        medium_wound_fixture.heal(recovery_result)
        return medium_wound_fixture
    @pytest.mark.parametrize("recovery_result, expected_wound_condition", [
        (wound_tracker.MediumWound._STABLE_EASE_FACTOR-1, wound_tracker.WoundStatus.WORSE),
        (wound_tracker.MediumWound._STABLE_EASE_FACTOR, wound_tracker.WoundStatus.SAME),
        (wound_tracker.MediumWound._RECOVERY_EASE_FACTOR, wound_tracker.WoundStatus.BETTER),
        (5, wound_tracker.WoundStatus.WORSE),
        (6, wound_tracker.WoundStatus.SAME),
        (12, wound_tracker.WoundStatus.BETTER),
    ])
    def test_medium_wound_healing(self,
            healed_medium_wound_fixture: wound_tracker.MediumWound,
            expected_wound_condition: wound_tracker.WoundStatus
        ):
        assert healed_medium_wound_fixture.status == expected_wound_condition
    @pytest.mark.parametrize("recovery_result, expected_bonus", [
        (wound_tracker.MediumWound._STABLE_EASE_FACTOR, wound_tracker.LightWound._STABLE_RECOVERY_BONUS),
        (wound_tracker.MediumWound._STABLE_EASE_FACTOR, 3),
    ])
    def test_medium_wound_stable_bonus(self,
            healed_medium_wound_fixture: wound_tracker.LightWound,
            expected_bonus: int
        ):
        assert healed_medium_wound_fixture.recovery_bonus == expected_bonus
    
    def test_heavy_wound_period(self, heavy_wound_fixture: wound_tracker.HeavyWound):
        assert heavy_wound_fixture.recovery_period == relativedelta.relativedelta(months=3)
    def test_heavy_wound_bonus(self, heavy_wound_fixture: wound_tracker.HeavyWound):
        assert heavy_wound_fixture.bonus == -5
    
    @pytest.fixture
    def healed_heavy_wound_fixture(self, heavy_wound_fixture: wound_tracker.HeavyWound, recovery_result: int):
        heavy_wound_fixture.heal(recovery_result)
        return heavy_wound_fixture
    @pytest.mark.parametrize("recovery_result, expected_wound_condition", [
        (wound_tracker.HeavyWound._STABLE_EASE_FACTOR-1, wound_tracker.WoundStatus.WORSE),
        (wound_tracker.HeavyWound._STABLE_EASE_FACTOR, wound_tracker.WoundStatus.SAME),
        (wound_tracker.HeavyWound._RECOVERY_EASE_FACTOR, wound_tracker.WoundStatus.BETTER),
        (8, wound_tracker.WoundStatus.WORSE),
        (9, wound_tracker.WoundStatus.SAME),
        (15, wound_tracker.WoundStatus.BETTER),
    ])
    def test_heavy_wound_healing(self,
            healed_heavy_wound_fixture: wound_tracker.HeavyWound,
            expected_wound_condition: wound_tracker.WoundStatus
        ):
        assert healed_heavy_wound_fixture.status == expected_wound_condition
    @pytest.mark.parametrize("recovery_result, expected_bonus", [
        (wound_tracker.HeavyWound._STABLE_EASE_FACTOR, wound_tracker.HeavyWound._STABLE_RECOVERY_BONUS),
        (wound_tracker.HeavyWound._STABLE_EASE_FACTOR, 3),
    ])
    def test_heavy_wound_stable_bonus(self,
            healed_heavy_wound_fixture: wound_tracker.HeavyWound,
            expected_bonus: int
        ):
        assert healed_heavy_wound_fixture.recovery_bonus == expected_bonus
    
    def test_incapacitating_wound_period(self, incapacitating_wound_fixture: wound_tracker.IncapacitatingWound):
        assert incapacitating_wound_fixture.recovery_period == relativedelta.relativedelta(hours=12)
    def test_incapacitating_wound_bonus(self, incapacitating_wound_fixture: wound_tracker.IncapacitatingWound):
        assert incapacitating_wound_fixture.bonus == None
    
    @pytest.fixture
    def healed_incapaciatated_wound_fixture(self, incapacitating_wound_fixture: wound_tracker.IncapacitatingWound, recovery_result: int):
        incapacitating_wound_fixture.heal(recovery_result)
        return incapacitating_wound_fixture
    @pytest.mark.parametrize("recovery_result, expected_wound_condition", [
        (wound_tracker.IncapacitatingWound._STABLE_EASE_FACTOR-1, wound_tracker.WoundStatus.WORSE),
        (wound_tracker.IncapacitatingWound._STABLE_EASE_FACTOR, wound_tracker.WoundStatus.SAME),
        (wound_tracker.IncapacitatingWound._RECOVERY_EASE_FACTOR, wound_tracker.WoundStatus.BETTER),
        (-1, wound_tracker.WoundStatus.WORSE),
        (0, wound_tracker.WoundStatus.SAME),
        (9, wound_tracker.WoundStatus.BETTER),
    ])
    def test_incapacitating_wound_healing(self,
            healed_incapaciatated_wound_fixture: wound_tracker.IncapacitatingWound,
            expected_wound_condition: wound_tracker.WoundStatus
        ):
        assert healed_incapaciatated_wound_fixture.status == expected_wound_condition
    @pytest.mark.parametrize("recovery_result, expected_bonus", [
        (wound_tracker.IncapacitatingWound._STABLE_EASE_FACTOR, wound_tracker.IncapacitatingWound._STABLE_RECOVERY_BONUS),
        (wound_tracker.IncapacitatingWound._STABLE_EASE_FACTOR, -1),
    ])
    def test_incapacitating_wound_stable_bonus(self,
            healed_incapaciatated_wound_fixture: wound_tracker.IncapacitatingWound,
            expected_bonus: int
        ):
        assert healed_incapaciatated_wound_fixture.recovery_bonus == expected_bonus

    def test_deadly_wound_period(self, deadly_wound_fixture: wound_tracker.DeadlyWound):
        assert deadly_wound_fixture.recovery_period == None
    def test_deadly_wound_bonus(self, deadly_wound_fixture: wound_tracker.DeadlyWound):
        assert deadly_wound_fixture.bonus == None
    def test_deadly_wound_recovery_bonus(self, deadly_wound_fixture: wound_tracker.DeadlyWound):
        assert deadly_wound_fixture.recovery_bonus == None

class TestWoundTracker():
    WOUND_FIXTURE_SIZE = 5
    WOUND_FIELDS_ARRAY = [
        "light_wounds",
        "medium_wounds",
        "heavy_wounds",
        "incapacitated",
        "dead",
    ]

    @pytest.fixture
    def wound_tracker_fixture(self) -> wound_tracker.WoundTracker:
        # subtract 5 because it gets normalized already in the wound tracker
        return wound_tracker.WoundTracker(size=self.WOUND_FIXTURE_SIZE-5)
    
    @pytest.fixture
    def wound_penalty_test_fixture(self, wound_tracker_fixture: wound_tracker.WoundTracker):
        wound_tracker_fixture._add_light_wound()
        wound_tracker_fixture._add_medium_wound()
        wound_tracker_fixture._add_heavy_wound()
        return wound_tracker_fixture
    
    @pytest.mark.parametrize("expected_penalty", [
        wound_tracker.HeavyWound.bonus+wound_tracker.MediumWound.bonus+wound_tracker.LightWound.bonus,
        -9
    ])
    def test_wound_tracker_penalty(self,
            wound_penalty_test_fixture: wound_tracker.WoundTracker,
            expected_penalty: int
        ):
        assert wound_penalty_test_fixture.wound_bonus == expected_penalty

    baseline_wounds = zip(WOUND_FIELDS_ARRAY, [# what does the wound tracker look like at baseline
        #light, medium, heavy, incap, dead
        0, 0, 0, False, False,
    ])
    
    @pytest.fixture(params=zip(WOUND_FIELDS_ARRAY, [
        WOUND_FIXTURE_SIZE,
        WOUND_FIXTURE_SIZE*2,
        WOUND_FIXTURE_SIZE*3,
        WOUND_FIXTURE_SIZE*4,
        WOUND_FIXTURE_SIZE*5,
    ]))
    def wounded_fixture_tuple(self, wound_tracker_fixture: wound_tracker.WoundTracker, request: pytest.FixtureRequest):
        wound_tracker_fixture.take_damage(request.param[1])
        return wound_tracker_fixture, request.param[0]
    @pytest.mark.parametrize("baseline_field, baseline_value", baseline_wounds)
    def test_wounding_no_extra_wounds(self,
            wounded_fixture_tuple: Tuple[wound_tracker.WoundTracker, str],
            baseline_field: str,
            baseline_value: int | Literal[False]
        ):
        wounded_fixture, wound_field = wounded_fixture_tuple
        if baseline_field == wound_field:
            pass
        else:
            assert wounded_fixture.model_computed_fields[baseline_field].wrapped_property.fget(wounded_fixture) == baseline_value
    def test_wounding_correct_wound_added(self,
            wounded_fixture_tuple: Tuple[wound_tracker.WoundTracker, str],
        ):
        wounded_fixture, wound_field = wounded_fixture_tuple
        assert wounded_fixture.model_computed_fields[wound_field].wrapped_property.fget(wounded_fixture)

    fully_wounded = zip(WOUND_FIELDS_ARRAY, [# what does the fully wounded wound tracker look like
        #light, medium, heavy, incap, dead
        1, 1, 1, True, True,
    ])

    def fully_wounded_fixture(self, wound_tracker_fixture: wound_tracker.WoundTracker):
        wound_tracker_fixture._add_light_wound()
        wound_tracker_fixture._add_medium_wound()
        wound_tracker_fixture._add_heavy_wound()
        wound_tracker_fixture._add_incapacitating_wound()
        wound_tracker_fixture._add_deadly_wound()
        return wound_tracker_fixture
    
    @pytest.mark.parametrize("recovery_result", [
        wound_tracker.LightWound._STABLE_EASE_FACTOR-1,
        wound_tracker.LightWound._STABLE_EASE_FACTOR,
        wound_tracker.LightWound._RECOVERY_EASE_FACTOR,
        3,
        4,
        10
    ])
    def test_light_wound_healing(self,
            fully_wounded_fixture: wound_tracker.WoundTracker,
            recovery_result: int
        ):
        fully_wounded_fixture.recover_all_light_wounds(recovery_result)
        
    


    # @pytest.mark.parametrize("baseline_field, baseline_value", baseline_wounds)
    # def test_wound_healing_correct_baseline_wounds(self,
    #         healed_fixture: wound_tracker.WoundTracker,
    #         baseline_field: str,
    #         baseline_value: int | Literal[False]
    #     ):
    #     assert healed_fixture.model_computed_fields[baseline_field].wrapped_property.fget(healed_fixture) == baseline_value