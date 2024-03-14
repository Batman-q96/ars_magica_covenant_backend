"""Tests for personality traits"""

import pytest

from characters import personality_trait


class TestPersonalityTrait:
    """Tests for the personality trait class implementation"""

    @pytest.fixture
    def personality_trait_fixture(self) -> personality_trait.PersonalityTrait:
        """Base fixture for further personality trait tests"""
        return personality_trait.PersonalityTrait(name="Test trait", intensity=-2)

    def test_create(self, personality_trait_fixture):
        """Test successful creation of personality traits"""
        assert personality_trait_fixture
