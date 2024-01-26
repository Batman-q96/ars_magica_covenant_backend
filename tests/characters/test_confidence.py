import pydantic
import pytest

from characters import confidence

class TestConfidence():
    @pytest.fixture
    def confidence_fixture(self) -> confidence.Confidence:
        return confidence.Confidence()
    
    def test_create(self, confidence_fixture):
        assert(confidence_fixture)
    
    def test_create_with_max(self):
        assert(confidence.Confidence(max=3))

    def test_create_with_max_and_points(self):
        assert(confidence.Confidence(points=3, max=3))

    def test_create_error_with_points_only(self):
        with pytest.raises(pydantic.ValidationError):
            confidence.Confidence(points=3)
    
    def test_points_below_0(self, confidence_fixture):
        with pytest.raises(pydantic.ValidationError):
            confidence_fixture.points -= 2
    
    def test_points_above_max(self, confidence_fixture):
        with pytest.raises(pydantic.ValidationError):
            confidence_fixture.points += 2
    
    def test_max_increase(self, confidence_fixture):
        confidence_fixture.max += 2
        confidence_fixture.points += 2
        assert(confidence_fixture.max == 2)
        assert(confidence_fixture.points == 2)
