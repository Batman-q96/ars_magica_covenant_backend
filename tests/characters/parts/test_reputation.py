"""Tests for reputation"""

import pytest

import pydantic


from characters.parts import reputation


class TestReputation:
    """Tests for the reputation class implementaiton"""

    @pytest.fixture
    def reputation_fixture(self) -> reputation.Reputation:
        """Base fixture for reputaiton testing"""
        return reputation.Reputation(content="Testing", target="Everyone")

    def test_create(self, reputation_fixture):
        """Test creation of the base reputation fixutre"""
        assert reputation_fixture

    def test_create_error_negative_score(self):
        """Test that we can't create a reputation with negative score"""
        with pytest.raises(pydantic.ValidationError):
            reputation.Reputation(score=-1, content="Testing", target="Everyone")

    def test_create_error_too_many_deeds(self):
        """Test taht we can't create a reputation with deeds exceeding the score"""
        with pytest.raises(pydantic.ValidationError):
            reputation.Reputation(
                score=1, deeds=10, content="Testing", target="Everyone"
            )

    def test_add_too_many_deeds(self, reputation_fixture: reputation.Reputation):
        """Test that we can't directly add deeds to exceed the reputation score"""
        with pytest.raises(pydantic.ValidationError):
            reputation_fixture.deeds += 10

    def test_add_reputation_properly(self, reputation_fixture: reputation.Reputation):
        """Test that adding in deeds correctly will adjust the repuation score as desired"""
        reputation_fixture.add_deeds(15)
        assert reputation_fixture.score == 2
        assert reputation_fixture.deeds == 5
