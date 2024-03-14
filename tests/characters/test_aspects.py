"""Tests for aspects"""

import pytest

from characters import aspect


class TestAspect:
    """Base Aspect tests"""

    @pytest.fixture
    def test_aspect_fixture(self) -> aspect.Aspect:
        """Aspect fixture for testing"""
        return aspect.Aspect(scale="Major", tag="General", content="", name="Test")

    def test_create(self, test_aspect_fixture):
        """Test creation of the base fixture"""
        assert test_aspect_fixture


class TestVirtue:
    """Virtue specific tests"""

    @pytest.fixture
    def test_virtue_fixture(self) -> aspect.Virtue:
        """Virtue fixture for testing"""
        return aspect.Virtue(scale="Major", tag="General", content="", name="Test")

    def test_create(self, test_virtue_fixture):
        """Test creation of the virtue fixture"""
        assert test_virtue_fixture


class TestFlaw:
    """Flaw specific tests"""

    @pytest.fixture
    def test_flaw_fixture(self) -> aspect.Flaw:
        """Base flaw fixture for testing"""
        return aspect.Flaw(scale="Major", tag="General", content="", name="Test")

    def test_create(self, test_flaw_fixture):
        """Test creation of the base flaw fixture"""
        assert test_flaw_fixture
