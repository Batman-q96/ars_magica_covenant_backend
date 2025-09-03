import pytest

from lib.leveled_trackers.base_leveled_tracker import BaseLeveledTracker


class DummyLeveledTracker(BaseLeveledTracker):
    def max_points(self):
        pass

    def add_points(self, points_to_gain: int) -> None:
        pass


def test_instantiation():
    tracker = DummyLeveledTracker(name="Test", level=2, points=1)
    assert tracker.name == "Test"
    assert tracker.level == 2
    assert tracker.points == 1


def test_abstract_methods_raise():
    with pytest.raises(TypeError):
        BaseLeveledTracker(name="Base")
