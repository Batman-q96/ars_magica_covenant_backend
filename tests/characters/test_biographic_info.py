"""Tests for biographic info"""

import pytest

from characters import biographic_info


class TestBiographicInfo:
    """Tests for the BiographicInfo container class"""

    @pytest.fixture
    def biographic_info_fixture(self) -> biographic_info.BiographicInfo:
        """Basic test fixture for further testing of biographic info"""
        return biographic_info.BiographicInfo()

    def test_create(self, biographic_info_fixture):
        """Test succesful creation of the base test fixture"""
        assert biographic_info_fixture
