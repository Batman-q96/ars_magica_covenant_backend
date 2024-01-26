import pydantic
import pytest

from characters import characterstics

@pytest.fixture
def characteristic_fixture() -> characterstics.Characteristics:
    return characterstics.Characteristics()

def test_create(characteristic_fixture):
    assert(characteristic_fixture)