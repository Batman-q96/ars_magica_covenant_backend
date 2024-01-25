from typing import Literal
import datetime

import pydantic


class FatigueTracker(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(validate_assignment=True)
    short_term_levels: int = pydantic.Field(default=0, ge=0)
    long_term_levels: int = pydantic.Field(default=0, ge=0)

    @pydantic.computed_field
    @property
    def penalty(self) -> int | bool:
        total_fatigue_levels = self.short_term_levels+self.long_term_levels
        if total_fatigue_levels <= 1:
            return 0
        elif total_fatigue_levels == 2:
            return 1
        elif total_fatigue_levels == 3:
            return 3
        elif total_fatigue_levels == 4:
            return 5
        elif total_fatigue_levels >= 5:
            return False
        else:
            raise RuntimeError
    
    @pydantic.computed_field
    @property
    def fatigue_level(self) -> Literal["Fresh", "Winded", "Weary", "Tired", "Dazed", "Unconscious"]:
        total_fatigue_levels = self.short_term_levels+self.long_term_levels
        if total_fatigue_levels == 0:
            return "Fresh"
        elif total_fatigue_levels == 1:
            return "Winded"
        elif total_fatigue_levels == 2:
            return "Weary"
        elif total_fatigue_levels == 3:
            return "Tired"
        elif total_fatigue_levels == 4:
            return "Dazed"
        elif total_fatigue_levels >= 5:
            return "Unconscious"
        else:
            raise ValueError("Total fatigue levels are negative")

    def get_short_term_recovery_time(self) -> datetime.timedelta:
        if self.short_term_levels == 0:
            # if we have no short term fatigue levels then we can't recover any
            raise ValueError
        else:
            total_fatigue_levels = self.short_term_levels+self.long_term_levels
            if total_fatigue_levels == 1:
                recovery_time = datetime.timedelta(minutes=2)
            elif total_fatigue_levels == 2:
                recovery_time = datetime.timedelta(minutes=10)
            elif total_fatigue_levels == 3:
                recovery_time = datetime.timedelta(minutes=30)
            elif total_fatigue_levels > 3:
                recovery_time = datetime.timedelta(hours=total_fatigue_levels-3)
            else:
                raise ValueError
        return recovery_time