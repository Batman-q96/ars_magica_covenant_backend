"""Tests for wounds and wound tracker"""

# pylint: disable=W0212

from typing import Literal, Tuple

import pytest

from dateutil import relativedelta

from characters.parts import wound_tracker

from lib import am5_rolls


def botch_roll(*args, **kwargs):
    """Helper function to simulate a botched roll"""
    raise am5_rolls.BotchedRollExcption(botch_level=0)


class TestWounds:
    """Tests for the various wounds"""

    @pytest.fixture
    def light_wound_fixture(self):
        """Fixture for testing things related to light wounds"""
        return wound_tracker.LightWound()

    @pytest.fixture
    def medium_wound_fixture(self):
        """Fixture for testing things related to medium wounds"""
        return wound_tracker.MediumWound()

    @pytest.fixture
    def heavy_wound_fixture(self):
        """Fixture for testing things related to heavy wounds"""
        return wound_tracker.HeavyWound()

    @pytest.fixture
    def incapacitating_wound_fixture(self):
        """Fixture for testing things related to incapacitating wounds"""
        return wound_tracker.IncapacitatingWound()

    @pytest.fixture
    def fatal_wound_fixture(self):
        """Fixture for testing things related to fatal wounds"""
        return wound_tracker.FatalWound()

    def test_light_wound_period(self, light_wound_fixture: wound_tracker.LightWound):
        """Test that the recovery period for light wounds is 1 week"""
        assert light_wound_fixture.recovery_period == relativedelta.relativedelta(
            weeks=1
        )

    def test_light_wound_bonus(self, light_wound_fixture: wound_tracker.LightWound):
        """Test that light woudns have a penalty of 1 each"""
        assert light_wound_fixture.bonus == -1

    @pytest.fixture
    def healed_light_wound_fixture(
        self, light_wound_fixture: wound_tracker.LightWound, recovery_result: int
    ):
        """Fixture for testing healing of light wounds"""
        light_wound_fixture.heal(recovery_result)
        return light_wound_fixture

    @pytest.mark.parametrize(
        "recovery_result, expected_wound_condition",
        [
            (
                wound_tracker.LightWound._STABLE_EASE_FACTOR - 1,
                wound_tracker.WoundStatus.WORSE,
            ),
            (
                wound_tracker.LightWound._STABLE_EASE_FACTOR,
                wound_tracker.WoundStatus.SAME,
            ),
            (
                wound_tracker.LightWound._RECOVERY_EASE_FACTOR,
                wound_tracker.WoundStatus.BETTER,
            ),
            (3, wound_tracker.WoundStatus.WORSE),
            (4, wound_tracker.WoundStatus.SAME),
            (10, wound_tracker.WoundStatus.BETTER),
        ],
    )
    def test_light_wound_healing(
        self,
        healed_light_wound_fixture: wound_tracker.LightWound,
        expected_wound_condition: wound_tracker.WoundStatus,
    ):
        """Test that the results of light wound recovery are what they should be based on level"""
        assert healed_light_wound_fixture.status == expected_wound_condition

    @pytest.mark.parametrize(
        "recovery_result, expected_bonus",
        [
            (
                wound_tracker.LightWound._STABLE_EASE_FACTOR,
                wound_tracker.LightWound._STABLE_RECOVERY_BONUS,
            ),
            (wound_tracker.LightWound._STABLE_EASE_FACTOR, 3),
        ],
    )
    def test_light_wound_stable_bonus(
        self, healed_light_wound_fixture: wound_tracker.LightWound, expected_bonus: int
    ):
        """Test that light wounds that don't get better become easier to heal"""
        assert healed_light_wound_fixture.recovery_bonus == expected_bonus

    def test_medium_wound_period(self, medium_wound_fixture: wound_tracker.MediumWound):
        """Test that medium wounds recover every month"""
        assert medium_wound_fixture.recovery_period == relativedelta.relativedelta(
            months=1
        )

    def test_medium_wound_bonus(self, medium_wound_fixture: wound_tracker.MediumWound):
        """Test that medium wounds apply the correct penalty"""
        assert medium_wound_fixture.bonus == -3

    @pytest.fixture
    def healed_medium_wound_fixture(
        self, medium_wound_fixture: wound_tracker.MediumWound, recovery_result: int
    ):
        """Fixture to test medium wound healing"""
        medium_wound_fixture.heal(recovery_result)
        return medium_wound_fixture

    @pytest.mark.parametrize(
        "recovery_result, expected_wound_condition",
        [
            (
                wound_tracker.MediumWound._STABLE_EASE_FACTOR - 1,
                wound_tracker.WoundStatus.WORSE,
            ),
            (
                wound_tracker.MediumWound._STABLE_EASE_FACTOR,
                wound_tracker.WoundStatus.SAME,
            ),
            (
                wound_tracker.MediumWound._RECOVERY_EASE_FACTOR,
                wound_tracker.WoundStatus.BETTER,
            ),
            (5, wound_tracker.WoundStatus.WORSE),
            (6, wound_tracker.WoundStatus.SAME),
            (12, wound_tracker.WoundStatus.BETTER),
        ],
    )
    def test_medium_wound_healing(
        self,
        healed_medium_wound_fixture: wound_tracker.MediumWound,
        expected_wound_condition: wound_tracker.WoundStatus,
    ):
        """Test that medium wound healing proceeds as expected"""
        assert healed_medium_wound_fixture.status == expected_wound_condition

    @pytest.mark.parametrize(
        "recovery_result, expected_bonus",
        [
            (
                wound_tracker.MediumWound._STABLE_EASE_FACTOR,
                wound_tracker.LightWound._STABLE_RECOVERY_BONUS,
            ),
            (wound_tracker.MediumWound._STABLE_EASE_FACTOR, 3),
        ],
    )
    def test_medium_wound_stable_bonus(
        self, healed_medium_wound_fixture: wound_tracker.LightWound, expected_bonus: int
    ):
        """Test that medium wounds that stay stable become easier to heal as expected"""
        assert healed_medium_wound_fixture.recovery_bonus == expected_bonus

    def test_heavy_wound_period(self, heavy_wound_fixture: wound_tracker.HeavyWound):
        """Test that heavy wounds take one season to heal"""
        assert heavy_wound_fixture.recovery_period == relativedelta.relativedelta(
            months=3
        )

    def test_heavy_wound_bonus(self, heavy_wound_fixture: wound_tracker.HeavyWound):
        """Test that heavy wounds apply the expected penalty"""
        assert heavy_wound_fixture.bonus == -5

    @pytest.fixture
    def healed_heavy_wound_fixture(
        self, heavy_wound_fixture: wound_tracker.HeavyWound, recovery_result: int
    ):
        """Fixture for testing healing of heavy wounds"""
        heavy_wound_fixture.heal(recovery_result)
        return heavy_wound_fixture

    @pytest.mark.parametrize(
        "recovery_result, expected_wound_condition",
        [
            (
                wound_tracker.HeavyWound._STABLE_EASE_FACTOR - 1,
                wound_tracker.WoundStatus.WORSE,
            ),
            (
                wound_tracker.HeavyWound._STABLE_EASE_FACTOR,
                wound_tracker.WoundStatus.SAME,
            ),
            (
                wound_tracker.HeavyWound._RECOVERY_EASE_FACTOR,
                wound_tracker.WoundStatus.BETTER,
            ),
            (8, wound_tracker.WoundStatus.WORSE),
            (9, wound_tracker.WoundStatus.SAME),
            (15, wound_tracker.WoundStatus.BETTER),
        ],
    )
    def test_heavy_wound_healing(
        self,
        healed_heavy_wound_fixture: wound_tracker.HeavyWound,
        expected_wound_condition: wound_tracker.WoundStatus,
    ):
        """Test that healing of heavy wounds proceeds as expected"""
        assert healed_heavy_wound_fixture.status == expected_wound_condition

    @pytest.mark.parametrize(
        "recovery_result, expected_bonus",
        [
            (
                wound_tracker.HeavyWound._STABLE_EASE_FACTOR,
                wound_tracker.HeavyWound._STABLE_RECOVERY_BONUS,
            ),
            (wound_tracker.HeavyWound._STABLE_EASE_FACTOR, 3),
        ],
    )
    def test_heavy_wound_stable_bonus(
        self, healed_heavy_wound_fixture: wound_tracker.HeavyWound, expected_bonus: int
    ):
        """Test that heavy wounds that stay stable become easier to heal as expected"""
        assert healed_heavy_wound_fixture.recovery_bonus == expected_bonus

    def test_incapacitating_wound_period(
        self, incapacitating_wound_fixture: wound_tracker.IncapacitatingWound
    ):
        """Test that incapacitating wounds roll for recovery every 12 hours"""
        assert (
            incapacitating_wound_fixture.recovery_period
            == relativedelta.relativedelta(hours=12)
        )

    def test_incapacitating_wound_bonus(
        self, incapacitating_wound_fixture: wound_tracker.IncapacitatingWound
    ):
        """Test that incapacitating wounds have an effectively infinite penalty"""
        assert incapacitating_wound_fixture.bonus is None

    @pytest.fixture
    def healed_incapaciatated_wound_fixture(
        self,
        incapacitating_wound_fixture: wound_tracker.IncapacitatingWound,
        recovery_result: int,
    ):
        """Fixture to test incapactiating wound healing"""
        incapacitating_wound_fixture.heal(recovery_result)
        return incapacitating_wound_fixture

    @pytest.mark.parametrize(
        "recovery_result, expected_wound_condition",
        [
            (
                wound_tracker.IncapacitatingWound._STABLE_EASE_FACTOR - 1,
                wound_tracker.WoundStatus.WORSE,
            ),
            (
                wound_tracker.IncapacitatingWound._STABLE_EASE_FACTOR,
                wound_tracker.WoundStatus.SAME,
            ),
            (
                wound_tracker.IncapacitatingWound._RECOVERY_EASE_FACTOR,
                wound_tracker.WoundStatus.BETTER,
            ),
            (-1, wound_tracker.WoundStatus.WORSE),
            (0, wound_tracker.WoundStatus.SAME),
            (9, wound_tracker.WoundStatus.BETTER),
        ],
    )
    def test_incapacitating_wound_healing(
        self,
        healed_incapaciatated_wound_fixture: wound_tracker.IncapacitatingWound,
        expected_wound_condition: wound_tracker.WoundStatus,
    ):
        """Test that resutls of incapacitating wound healing are as we expect"""
        assert healed_incapaciatated_wound_fixture.status == expected_wound_condition

    @pytest.mark.parametrize(
        "recovery_result, expected_bonus",
        [
            (
                wound_tracker.IncapacitatingWound._STABLE_EASE_FACTOR,
                wound_tracker.IncapacitatingWound._STABLE_RECOVERY_BONUS,
            ),
            (wound_tracker.IncapacitatingWound._STABLE_EASE_FACTOR, -1),
        ],
    )
    def test_incapacitating_wound_stable_bonus(
        self,
        healed_incapaciatated_wound_fixture: wound_tracker.IncapacitatingWound,
        expected_bonus: int,
    ):
        """Test that incapacitaing woudns get worse over time if they stay stable"""
        assert healed_incapaciatated_wound_fixture.recovery_bonus == expected_bonus

    def test_fatal_wound_period(self, fatal_wound_fixture: wound_tracker.FatalWound):
        """Test that fatal wounds don't heal naturally"""
        assert fatal_wound_fixture.recovery_period is None

    def test_fatal_wound_bonus(self, fatal_wound_fixture: wound_tracker.FatalWound):
        """Test that fatal wounds have an effectively infinite penalty"""
        assert fatal_wound_fixture.bonus is None

    def test_deadly_wound_recovery_bonus(
        self, fatal_wound_fixture: wound_tracker.FatalWound
    ):
        """Test that fatal wounds don't have a recovery bonus"""
        assert fatal_wound_fixture.recovery_bonus is None


class TestWoundTracker:
    """Tests for the wound tracker"""

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
        """Fixture for futher tests with the wound tracker"""
        # subtract 5 because it gets normalized already in the wound tracker
        return wound_tracker.WoundTracker(size=self.WOUND_FIXTURE_SIZE - 5)

    @pytest.fixture
    def wound_penalty_test_fixture(
        self, wound_tracker_fixture: wound_tracker.WoundTracker
    ):
        """Fixture with wounds added for testing"""
        wound_tracker_fixture._add_light_wound()
        wound_tracker_fixture._add_medium_wound()
        wound_tracker_fixture._add_heavy_wound()
        return wound_tracker_fixture

    @pytest.mark.parametrize(
        "expected_penalty",
        [
            wound_tracker.HeavyWound.bonus
            + wound_tracker.MediumWound.bonus
            + wound_tracker.LightWound.bonus,
            -9,
        ],
    )
    def test_wound_tracker_penalty(
        self,
        wound_penalty_test_fixture: wound_tracker.WoundTracker,
        expected_penalty: int,
    ):
        """Check the penalty of the wound tracker is what we expect given the wounds it has"""
        assert wound_penalty_test_fixture.wound_bonus == expected_penalty

    baseline_wounds = zip(
        WOUND_FIELDS_ARRAY,
        [  # what does the wound tracker look like at baseline
            # light, medium, heavy, incap, dead
            0,
            0,
            0,
            False,
            False,
        ],
    )

    class TestWounding:
        """Test wounds get added correctly to the wound tracker"""

    @pytest.fixture(
        params=zip(
            WOUND_FIELDS_ARRAY,
            [
                WOUND_FIXTURE_SIZE,
                WOUND_FIXTURE_SIZE * 2,
                WOUND_FIXTURE_SIZE * 3,
                WOUND_FIXTURE_SIZE * 4,
                WOUND_FIXTURE_SIZE * 5,
            ],
        )
    )
    def wounded_fixture_tuple(
        self,
        wound_tracker_fixture: wound_tracker.WoundTracker,
        request: pytest.FixtureRequest,
    ):
        """Check that wounds get added to the fixture as expected"""
        wound_tracker_fixture.take_damage(request.param[1])
        return wound_tracker_fixture, request.param[0]

    @pytest.mark.parametrize("baseline_field, baseline_value", baseline_wounds)
    def test_wounding_no_extra_wounds(
        self,
        wounded_fixture_tuple: Tuple[wound_tracker.WoundTracker, str],
        baseline_field: str,
        baseline_value: int | Literal[False],
    ):
        """Test that wounding doesn't add extraneous wounds"""
        wounded_fixture, wound_field = wounded_fixture_tuple
        if baseline_field == wound_field:
            pass
        else:
            assert (
                wounded_fixture.model_computed_fields[
                    baseline_field
                ].wrapped_property.fget(wounded_fixture)
                == baseline_value
            )

    def test_wounding_correct_wound_added(
        self,
        wounded_fixture_tuple: Tuple[wound_tracker.WoundTracker, str],
    ):
        """Test that wounding adds the desired wound correctly"""
        wounded_fixture, wound_field = wounded_fixture_tuple
        assert wounded_fixture.model_computed_fields[wound_field].wrapped_property.fget(
            wounded_fixture
        )

    fully_wounded = zip(
        WOUND_FIELDS_ARRAY,
        [  # what does the fully wounded wound tracker look like
            # light, medium, heavy, incap, dead
            1,
            1,
            1,
            True,
            True,
        ],
    )

    class TestLightWoundHealing:
        """Tests for healing light wounds"""

        @pytest.fixture
        def light_wound_fixture(
            self, wound_tracker_fixture: wound_tracker.WoundTracker
        ):
            """Fixture containing a light wound to be healed"""
            wound_tracker_fixture.add_wound(wound_tracker.LightWound())
            return wound_tracker_fixture

        @pytest.mark.parametrize(
            "recovery_result",
            [wound_tracker.LightWound._STABLE_EASE_FACTOR - 1, 3],
        )
        def test_light_wound_gets_worse(
            self,
            light_wound_fixture: wound_tracker.WoundTracker,
            recovery_result: int,
        ):
            """Test light wounds get worse correctly in the tracker"""
            light_wound_fixture.recover_all_light_wounds(0, recovery_result)
            assert light_wound_fixture.light_wounds == 0
            assert light_wound_fixture.medium_wounds == 1

        @pytest.mark.parametrize(
            "recovery_result",
            [wound_tracker.LightWound._STABLE_EASE_FACTOR, 4],
        )
        def test_light_wound_stays_the_same(
            self,
            light_wound_fixture: wound_tracker.WoundTracker,
            recovery_result: int,
        ):
            """Test light wounds stay the same correctly"""
            light_wound_fixture.recover_all_light_wounds(0, recovery_result)
            assert light_wound_fixture.light_wounds == 1
            assert light_wound_fixture._light_wounds[0].recovery_bonus == 3

        @pytest.mark.parametrize(
            "recovery_result",
            [wound_tracker.LightWound._RECOVERY_EASE_FACTOR, 10],
        )
        def test_light_wound_gets_better(
            self,
            light_wound_fixture: wound_tracker.WoundTracker,
            recovery_result: int,
        ):
            """Test that light wounds get better correctly"""
            light_wound_fixture.recover_all_light_wounds(0, recovery_result)
            assert light_wound_fixture.light_wounds == 0

    class TestMediumWoundHealing:
        """Tests for healing medium wounds"""

        @pytest.fixture
        def medium_wound_fixture(
            self, wound_tracker_fixture: wound_tracker.WoundTracker
        ):
            """Fixture containing a medium wound to be healed"""
            wound_tracker_fixture.add_wound(wound_tracker.MediumWound())
            return wound_tracker_fixture

        @pytest.mark.parametrize(
            "recovery_result",
            [wound_tracker.MediumWound._STABLE_EASE_FACTOR - 1, 5],
        )
        def test_medium_wound_gets_worse(
            self,
            medium_wound_fixture: wound_tracker.WoundTracker,
            recovery_result: int,
        ):
            """Test medium wounds get worse correctly in the tracker"""
            medium_wound_fixture.recover_all_medium_wounds(0, recovery_result)
            assert medium_wound_fixture.medium_wounds == 0
            assert medium_wound_fixture.heavy_wounds == 1

        @pytest.mark.parametrize(
            "recovery_result",
            [wound_tracker.MediumWound._STABLE_EASE_FACTOR, 6],
        )
        def test_medium_wound_stays_the_same(
            self,
            medium_wound_fixture: wound_tracker.WoundTracker,
            recovery_result: int,
        ):
            """Test medium wounds stay the same correctly"""
            medium_wound_fixture.recover_all_medium_wounds(0, recovery_result)
            assert medium_wound_fixture.medium_wounds == 1
            assert medium_wound_fixture._medium_wounds[0].recovery_bonus == 3

        @pytest.mark.parametrize(
            "recovery_result",
            [wound_tracker.MediumWound._RECOVERY_EASE_FACTOR, 12],
        )
        def test_medium_wound_gets_better(
            self,
            medium_wound_fixture: wound_tracker.WoundTracker,
            recovery_result: int,
        ):
            """Test that medium wounds get better correctly"""
            medium_wound_fixture.recover_all_medium_wounds(0, recovery_result)
            assert medium_wound_fixture.medium_wounds == 0
            assert medium_wound_fixture.light_wounds == 1

    class TestHeavyWoundHealing:
        """Tests for healing medium wounds"""

        @pytest.fixture
        def heavy_wound_fixture(
            self, wound_tracker_fixture: wound_tracker.WoundTracker
        ):
            """Fixture containing a medium wound to be healed"""
            wound_tracker_fixture.add_wound(wound_tracker.HeavyWound())
            return wound_tracker_fixture

        @pytest.mark.parametrize(
            "recovery_result",
            [wound_tracker.HeavyWound._STABLE_EASE_FACTOR - 1, 8],
        )
        def test_heavy_wound_gets_worse(
            self,
            heavy_wound_fixture: wound_tracker.WoundTracker,
            recovery_result: int,
        ):
            """Test heavy wounds get worse correctly in the tracker"""
            heavy_wound_fixture.recover_all_heavy_wounds(0, recovery_result)
            assert heavy_wound_fixture.heavy_wounds == 0
            assert heavy_wound_fixture.incapacitated is True

        @pytest.mark.parametrize(
            "recovery_result",
            [wound_tracker.HeavyWound._STABLE_EASE_FACTOR, 9],
        )
        def test_heavy_wound_stays_the_same(
            self,
            heavy_wound_fixture: wound_tracker.WoundTracker,
            recovery_result: int,
        ):
            """Test heavy wounds stay the same correctly"""
            heavy_wound_fixture.recover_all_heavy_wounds(0, recovery_result)
            assert heavy_wound_fixture.heavy_wounds == 1
            assert heavy_wound_fixture._heavy_wounds[0].recovery_bonus == 3

        @pytest.mark.parametrize(
            "recovery_result",
            [wound_tracker.HeavyWound._RECOVERY_EASE_FACTOR, 15],
        )
        def test_heavy_wound_gets_better(
            self,
            heavy_wound_fixture: wound_tracker.WoundTracker,
            recovery_result: int,
        ):
            """Test that heavy wounds get better correctly"""
            heavy_wound_fixture.recover_all_heavy_wounds(0, recovery_result)
            assert heavy_wound_fixture.heavy_wounds == 0
            assert heavy_wound_fixture.medium_wounds == 1

    class TestIncapacitatingWoundHealing:
        """Tests for healing incapacitating wounds"""

        @pytest.fixture
        def incapacitating_wound_fixture(
            self, wound_tracker_fixture: wound_tracker.WoundTracker
        ):
            """Fixture containing a medium wound to be healed"""
            wound_tracker_fixture.add_wound(wound_tracker.IncapacitatingWound())
            return wound_tracker_fixture

        @pytest.mark.parametrize(
            "recovery_result",
            [wound_tracker.IncapacitatingWound._STABLE_EASE_FACTOR - 1, -1],
        )
        def test_incapcitating_wound_gets_worse(
            self,
            incapacitating_wound_fixture: wound_tracker.WoundTracker,
            recovery_result: int,
        ):
            """Test heavy wounds get worse correctly in the tracker"""
            incapacitating_wound_fixture.recover_all_incapacitating_wounds(
                0, recovery_result
            )
            assert incapacitating_wound_fixture.incapacitated is False
            assert incapacitating_wound_fixture.dead is True

        @pytest.mark.parametrize(
            "recovery_result",
            [wound_tracker.IncapacitatingWound._STABLE_EASE_FACTOR, 0],
        )
        def test_incapcitating_wound_stays_the_same(
            self,
            incapacitating_wound_fixture: wound_tracker.WoundTracker,
            recovery_result: int,
        ):
            """Test heavy wounds stay the same correctly"""
            incapacitating_wound_fixture.recover_all_incapacitating_wounds(
                0, recovery_result
            )
            assert incapacitating_wound_fixture.incapacitated is True
            assert incapacitating_wound_fixture._incapacitating_wound
            assert (
                incapacitating_wound_fixture._incapacitating_wound.recovery_bonus == -1
            )

        @pytest.mark.parametrize(
            "recovery_result",
            [wound_tracker.IncapacitatingWound._RECOVERY_EASE_FACTOR, 9],
        )
        def test_incapcitating_wound_gets_better(
            self,
            incapacitating_wound_fixture: wound_tracker.WoundTracker,
            recovery_result: int,
        ):
            """Test that heavy wounds get better correctly"""
            incapacitating_wound_fixture.recover_all_incapacitating_wounds(
                0, recovery_result
            )
            assert incapacitating_wound_fixture.incapacitated is False
            assert incapacitating_wound_fixture.heavy_wounds == 1

    class TestFatalWoundHealing:
        """Tests for healing of fatal wounds, curently empty as fatal wounds can't heal naturally"""
