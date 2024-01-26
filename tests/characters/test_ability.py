import pytest
import pydantic

from characters import ability

class TestAbility():
        
    @pytest.fixture
    def ability_fixture(self) -> ability.Ability:
        return ability.Ability(name="Test Ability")

    def test_create(self, ability_fixture: ability.Ability):
        assert(ability_fixture)
    
    def test_create_with_experience(self):
        assert(ability.Ability(name="Test Ability", experience=2))
    
    def test_create_with_level(self):
        assert(ability.Ability(name="Test Ability", experience=2))
    
    def test_create_with_level_and_experience(self):
        assert(ability.Ability(name="Test Ability", experience=12, level=2))

    def test_create_error_negative_experience(self):
        with pytest.raises(pydantic.ValidationError):
            ability.Ability(name="Test Ability", experience=-2)

    def test_create_error_too_much_experience(self):
        with pytest.raises(pydantic.ValidationError):
            ability.Ability(name="Test Ability", experience=12)

    def test_add_too_much_experience(self, ability_fixture: ability.Ability):
        with pytest.raises(pydantic.ValidationError):
            ability_fixture.experience+=20

    def test_add_experience(self, ability_fixture: ability.Ability):
        ability_fixture.add_experience(20)
        assert(ability_fixture.level==2)
        assert(ability_fixture.experience==5)