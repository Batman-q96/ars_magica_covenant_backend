import pydantic
import pytest

from src.characters import biographic_info

class TestBiographicInfo():
    @pytest.fixture
    def biographic_info_fixture(self) -> biographic_info.BiographicInfo:
        return biographic_info.BiographicInfo()
    
    def test_create(self, biographic_info_fixture):
        assert(biographic_info_fixture)