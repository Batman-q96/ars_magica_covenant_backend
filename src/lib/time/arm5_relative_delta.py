"""Common functions to help with processing time"""

from typing import Optional
import datetime

from dateutil import relativedelta


class Arm5RelativeDelta(relativedelta.relativedelta):
    """
    A relativedelta specific to Ars Magica 5th edition.
    Additional features it has are comparing among each other, supporting seasons
    and converting with weeks and months via approximations.
    """
