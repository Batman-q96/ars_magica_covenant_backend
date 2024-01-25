import pytest
import pydantic

from src.characters import abilities

class TestAbility():
        
    @pytest.fixture
    def ability_fixture(self) -> abilities.Ability:
        return abilities.Ability(name="Test Ability")

    def test_create(self, ability_fixture: abilities.Ability):
        assert(ability_fixture)
    
    def test_create_with_experience(self):
        assert(abilities.Ability(name="Test Ability", experience=2))
    
    def test_create_with_level(self):
        assert(abilities.Ability(name="Test Ability", experience=2))
    
    def test_create_with_level_and_experience(self):
        assert(abilities.Ability(name="Test Ability", experience=12, level=2))

    def test_create_error_negative_experience(self):
        with pytest.raises(pydantic.ValidationError):
            abilities.Ability(name="Test Ability", experience=-2)

    def test_create_error_too_much_experience(self):
        with pytest.raises(pydantic.ValidationError):
            abilities.Ability(name="Test Ability", experience=12)

    def test_add_too_much_experience(self, ability_fixture: abilities.Ability):
        with pytest.raises(pydantic.ValidationError):
            ability_fixture.experience+=20

    def test_add_experience(self, ability_fixture: abilities.Ability):
        ability_fixture.add_experience(20)
        assert(ability_fixture.level==2)
        assert(ability_fixture.experience==5)