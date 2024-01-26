import pytest

from characters import aspect

class TestAspect():
    @pytest.fixture
    def test_aspect_fixture(self) -> aspect.Aspect:
        return aspect.Aspect(scale="Major", tag="General", content="", name="Test")
    
    def test_create(self, test_aspect_fixture):
        assert(test_aspect_fixture)
    
class TestFlaw():
    @pytest.fixture
    def test_flaw_fixture(self) -> aspect.Flaw:
        return aspect.Flaw(scale="Major", tag="General", content="", name="Test")
    
    def test_create(self, test_flaw_fixture):
        assert(test_flaw_fixture)