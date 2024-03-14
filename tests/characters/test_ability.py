"""Tests for abilities"""

import pytest
import pydantic

from characters import ability


class TestAbility:
    """Tests for the ability class"""

    @pytest.fixture
    def ability_fixture(self) -> ability.Ability:
        """Create an ability fixture for testing"""
        return ability.Ability(name="Test Ability")

    def test_create(self, ability_fixture: ability.Ability):
        """Test creation of an ability"""
        assert ability_fixture

    def test_create_with_experience(self):
        """Test creation with some base experience"""
        assert ability.Ability(name="Test Ability", experience=2)

    def test_create_with_level(self):
        """Test creation with some base level"""
        assert ability.Ability(name="Test Ability", experience=2)

    def test_create_with_level_and_experience(self):
        """Test creation with some base level and experience"""
        assert ability.Ability(name="Test Ability", experience=12, level=2)

    def test_create_error_negative_experience(self):
        """Test that we can't create with negative experience"""
        with pytest.raises(pydantic.ValidationError):
            ability.Ability(name="Test Ability", experience=-2)

    def test_create_error_too_much_experience(self):
        """Test that we can't create with experience higher than max allowed by level"""
        with pytest.raises(pydantic.ValidationError):
            ability.Ability(name="Test Ability", experience=12)

    def test_add_too_much_experience(self, ability_fixture: ability.Ability):
        """Test that we can't add too much experience"""
        with pytest.raises(pydantic.ValidationError):
            ability_fixture.experience += 20

    def test_add_experience(self, ability_fixture: ability.Ability):
        """Test that we can add too much experience using add_experience"""
        ability_fixture.add_experience(20)
        assert ability_fixture.level == 2
        assert ability_fixture.experience == 5
