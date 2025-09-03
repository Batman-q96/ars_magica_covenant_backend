"""Common functions to help with processing time"""

import datetime

from dateutil import relativedelta


class Arm5RelativeDelta(relativedelta.relativedelta):
    """
    A relativedelta specific to Ars Magica 5th edition, primarily used for durations.
    Additional features it has are comparing among each other, supporting seasons
    and converting with weeks and months via approximations.

    It does away with aboslute dates, as they are not used in durations.
    """

    def __init__(
        self,
        dt1: datetime.date | None = None,
        dt2: datetime.date | None = None,
        years: int = 0,
        seasons: int = 0,
        months: int = 0,
        days: int = 0,
        leapdays: int = 0,
        weeks: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        microseconds: int = 0,
    ) -> None:
        months += seasons * 3
        super().__init__(
            dt1,
            dt2,
            years,
            months,
            days,
            leapdays,
            weeks,
            hours,
            minutes,
            seconds,
            microseconds,
        )

    @property
    def seasons(self) -> int:
        """Get the number of seasons in this delta"""
        return self.months // 3

    def __lt__(self, other: "Arm5RelativeDelta") -> bool:
        """Check if this delta is less than another"""
        if not isinstance(other, Arm5RelativeDelta):
            return NotImplemented
        # Compare years
        if self.years != other.years:
            return self.years < other.years
        # Compare months
        if self.months != other.months:
            return self.months < other.months
        # Compare days
        if self.days != other.days:
            return self.days < other.days
        # Compare hours
        if self.hours != other.hours:
            return self.hours < other.hours
        # Compare minutes
        if self.minutes != other.minutes:
            return self.minutes < other.minutes
        # Compare seconds
        if self.seconds != other.seconds:
            return self.seconds < other.seconds
        # Compare microseconds
        return self.microseconds < other.microseconds

    def __le__(self, other: "Arm5RelativeDelta") -> bool:
        """Check if this delta is less than or equal to another"""
        if not isinstance(other, Arm5RelativeDelta):
            return NotImplemented
        return self < other or self == other

    def __gt__(self, other: "Arm5RelativeDelta") -> bool:
        """Check if this delta is greater than another"""
        if not isinstance(other, Arm5RelativeDelta):
            return NotImplemented
        return not self <= other

    def __ge__(self, other: "Arm5RelativeDelta") -> bool:
        """Check if this delta is greater than or equal to another"""
        if not isinstance(other, Arm5RelativeDelta):
            return NotImplemented
        return not self < other
