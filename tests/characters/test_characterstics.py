import pydantic
import pytest

from src.characters import characterstics

@pytest.fixture
def characteristic_fixture() -> characterstics.Characteristics:
    return characterstics.Characteristics()

def test_create(characteristic_fixture):
    assert(characteristic_fixture)