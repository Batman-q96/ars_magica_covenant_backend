from lib.leveled_trackers import base_leveled_tracker


class LeveledTrackerX5(base_leveled_tracker.BaseLeveledTracker):
    def max_points(self):
        assert self.points < 5 * (self.level + 1)
        return self

    def add_points(self, points_to_gain: int) -> None:
        new_points = self.points + points_to_gain
        if new_points >= 0:
            while new_points >= 5 * (self.level + 1):
                new_points -= 5 * (self.level + 1)
                self.level += 1
        else:
            while new_points <= 5 * (self.level + 1):
                new_points += 5 * (self.level + 1)
                self.level -= 1
        self.points = new_points
