"""Common functions to help with processing time"""

from typing import Optional
import datetime

from lib.time import arm5_relative_delta

# Common helper durations
SEASON = arm5_relative_delta.Arm5RelativeDelta(seasons=1)
MONTH = arm5_relative_delta.Arm5RelativeDelta(months=1)
MOON = arm5_relative_delta.Arm5RelativeDelta(months=1)
WEEK = arm5_relative_delta.Arm5RelativeDelta(weeks=1)
DAY = arm5_relative_delta.Arm5RelativeDelta(days=1)
SUN = arm5_relative_delta.Arm5RelativeDelta(hours=12)
HOUR = arm5_relative_delta.Arm5RelativeDelta(hours=1)
DIAMETER = arm5_relative_delta.Arm5RelativeDelta(minutes=2)
MINUTE = arm5_relative_delta.Arm5RelativeDelta(minutes=1)
