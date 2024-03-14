"""Tests for characterstics"""

import pytest

from characters import characterstics


class TestCharacterstics:
    """Test class for characterstic container class"""

    @pytest.fixture
    def characteristic_fixture(self) -> characterstics.Characteristics:
        """Base testing fixture for characterstics"""
        return characterstics.Characteristics()

    def test_create(self, characteristic_fixture):
        """Test characterstic creation"""
        assert characteristic_fixture
