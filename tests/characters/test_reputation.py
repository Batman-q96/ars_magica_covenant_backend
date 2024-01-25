import pytest

import pydantic


from src.characters import reputation

class TestReputation():
    @pytest.fixture
    def reputation_fixture(self) -> reputation.Reputation:
        return reputation.Reputation(content="Testing", target="Everyone")
    
    def test_create(self, reputation_fixture):
        assert(reputation_fixture)

    def test_create_error_negative_score(self):
        with pytest.raises(pydantic.ValidationError):
            reputation.Reputation(score=-1, content="Testing", target="Everyone")
    
    def test_create_error_too_many_deeds(self):
        with pytest.raises(pydantic.ValidationError):
            reputation.Reputation(score=1, deeds=10, content="Testing", target="Everyone")

    def test_add_too_many_deeds(self, reputation_fixture: reputation.Reputation):
        with pytest.raises(pydantic.ValidationError):
            reputation_fixture.deeds+=10

    def test_add_reputation_properly(self, reputation_fixture: reputation.Reputation):
        reputation_fixture.add_deeds(15)
        assert(reputation_fixture.score == 2)
        assert(reputation_fixture.deeds == 5)