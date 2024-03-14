"""Tests for characterstics"""

import pytest

from characters.parts import characterstics


class TestCharacterstics:
    """Test class for characterstic container class"""

    @pytest.fixture
    def characteristic_fixture(self) -> characterstics.Characteristics:
        """Base testing fixture for characterstics"""
        return characterstics.Characteristics()

    def test_create(self, characteristic_fixture):
        """Test characterstic creation"""
        assert characteristic_fixture

    @pytest.mark.parametrize(
        "char_name",
        [
            "strength",
            "stamina",
            "quickness",
            "dexterity",
            "intelligence",
            "perception",
            "presence",
            "communication",
        ],
    )
    def test_iterate_names(self, char_name: str):
        """Make sure we return every characterstic when iterating over the names"""
        assert char_name in characterstics.Characteristics.iter_char_names()

    def test_iterate_over_fixture(
        self, characteristic_fixture: characterstics.Characteristics
    ):
        """Make sure all the characterstics were properly set to 0"""
        for _, value in characteristic_fixture:
            assert value == 0

    @pytest.mark.parametrize(
        ("values", "expected_value"), [([3], 6), ([1, 2], 4), ([3, 1], 7)]
    )
    def test_get_characterstics_point_cost(
        self,
        characteristic_fixture: characterstics.Characteristics,
        values: list[int],
        expected_value: int,
    ):
        """Make sure we can properly calculate point costs"""
        for value, (char_name, _) in zip(values, characteristic_fixture):
            characteristic_fixture.__dict__[char_name] = value
        assert characteristic_fixture.get_characterstics_point_cost() == expected_value

    @pytest.mark.parametrize(
        ("values", "target_value", "expected_value"),
        [
            ([3], 5, False),
            ([3], 7, True),
            ([3, 1], 7, True),
            ([3, 1], 5, False),
            ([-1, 1, 1, 1], 4, True),
            ([1, 1, 1, 1], 2, False),
            ([9, 1, 1, 1], 2, False),
        ],
    )
    def test_is_valid_starting_characterstics(
        self,
        characteristic_fixture: characterstics.Characteristics,
        values: list[int],
        target_value: int,
        expected_value: bool,
    ):
        """Test that we can properly determine if these characterstics are valid"""

        for value, (char_name, _) in zip(values, characteristic_fixture):
            characteristic_fixture.__dict__[char_name] = value

        assert (
            characteristic_fixture.is_valid_starting_characterstics(
                max_cost=target_value
            )
            == expected_value
        )

    @pytest.mark.parametrize(
        ("values", "target_value", "expected_value"),
        [
            ([3], 5, False),
            ([3], 7, False),
            ([3, 1], 7, True),
            ([3, 1], 8, False),
            ([1, 1, 1, 1], 4, True),
            ([1, 1, -1, 1], 2, True),
            ([-1, 1, -10, 1], 2, False),
        ],
    )
    def test_is_valid_starting_characterstics_and_fully_spent(
        self,
        characteristic_fixture: characterstics.Characteristics,
        values: list[int],
        target_value: int,
        expected_value: bool,
    ):
        """Test that we can properly determine if these characterstics are valid"""

        for value, (char_name, _) in zip(values, characteristic_fixture):
            characteristic_fixture.__dict__[char_name] = value

        assert (
            characteristic_fixture.is_valid_starting_characterstics_and_fully_spent(
                max_cost=target_value
            )
            == expected_value
        )

    def test_raises_extreme_characterstics_error(
        self, characteristic_fixture: characterstics.Characteristics
    ):
        """Test that we raise the extreme characterstics error on extreme values as expected"""
        characteristic_fixture.strength = 4
        with pytest.raises(characterstics.ExtremeCharactersticsError):
            characteristic_fixture.get_characterstics_point_cost()

    def test_add(self, characteristic_fixture: characterstics.Characteristics):
        """Test that we can add values to all characterstics"""
        for _, val in characteristic_fixture + 1:
            assert val == 1

    def test_sub(self, characteristic_fixture: characterstics.Characteristics):
        """Test that we can subtract values from all characterstics"""
        for _, val in characteristic_fixture - 1:
            assert val == -1
