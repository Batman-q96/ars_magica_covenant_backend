import pytest

from src.characters import personality_trait

class TestPersonalityTrait():
    @pytest.fixture
    def personality_trait_fixture(self) -> personality_trait.PersonalityTrait:
        return personality_trait.PersonalityTrait(name="Test trait", intensity=-2)
    
    def test_create(self, personality_trait_fixture):
        assert(personality_trait_fixture)