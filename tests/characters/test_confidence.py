"""Tests for confidence implementation"""

import pydantic
import pytest

from src.characters import confidence


class TestConfidence:
    """Tests for the confidence score class"""

    @pytest.fixture
    def confidence_fixture(self) -> confidence.Confidence:
        """Base test fixture for confidence score tests"""
        return confidence.Confidence()

    def test_create(self, confidence_fixture: confidence.Confidence):
        """Test creation of the confidence score class"""
        assert confidence_fixture

    def test_create_with_max(self):
        """Test creation with a non zero max"""
        assert confidence.Confidence(max=3)

    def test_create_with_max_and_points(self):
        """Test creation with non zero max and non zero points"""
        assert confidence.Confidence(points=3, max=3)

    def test_create_error_with_points_only(self):
        """Test that creating with poitns but not raising max will raise error"""
        with pytest.raises(pydantic.ValidationError):
            confidence.Confidence(points=3)

    def test_points_below_0(self, , confidence_fixture: confidence.Confidence):
        """Test that we can't have negative confidence points"""
        with pytest.raises(pydantic.ValidationError):
            confidence_fixture.points -= 2

    def test_points_above_max(self, confidence_fixture: confidence.Confidence):
        """Test that we can't raise opints above the max"""
        with pytest.raises(pydantic.ValidationError):
            confidence_fixture.points += 2

    def test_max_increase(self, confidence_fixture: confidence.Confidence):
        """Test that we can raise max and then raise poitns to the new max"""
        confidence_fixture.max += 2
        confidence_fixture.points += 2
        assert confidence_fixture.max == 2
        assert confidence_fixture.points == 2
