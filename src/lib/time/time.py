"""Common functions to help with processing time"""

from typing import Optional
import datetime

from dateutil import relativedelta


def get_deltas_in_larger_relative_delta(
    *,
    short_duration: Optional[relativedelta.relativedelta] = None,
    long_duration: relativedelta.relativedelta,
    start_date: Optional[datetime.datetime] = None,
) -> int:
    """Helper function to get the number of weeks in a relative delta because we
    can't easily convert between months and weeks"""
    short_duration = (
        relativedelta.relativedelta(weeks=1)
        if short_duration is None
        else short_duration
    )
    start_date = datetime.datetime.today() if start_date is None else start_date
    end_date = start_date + long_duration
    counter = -1  # this way we round down to the nearest full number of weeks
    while end_date > start_date:
        counter += 1
        end_date -= short_duration
    return counter


class Arm5RelativeDelta(relativedelta.relativedelta):
    """
    A relativedelta specific to Ars Magica 5th edition.
    Additional features it has are comparing among each other, supporting seasons
    and converting with weeks and months via approximations.
    """
