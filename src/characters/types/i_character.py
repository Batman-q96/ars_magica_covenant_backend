"""Character interface"""

from typing import Annotated, Optional

import abc
import datetime

import pydantic

from characters.parts import (
    ability as parts_ability,
    aspect as parts_aspect,
    biographic_info as parts_biographic_info,
    characterstics as parts_characterstics,
    confidence as parts_confidence,
    fatigue as parts_fatigue,
    personality_trait as parts_traits,
    reputation as parts_rep,
)


class ICharacter(abc.ABC, pydantic.BaseModel):
    """Character class interface"""

    characteristics: parts_characterstics.Characteristics = pydantic.Field(
        default_factory=parts_characterstics.Characteristics
    )
    confidence: parts_confidence.Confidence = pydantic.Field(
        default_factory=parts_confidence.Confidence
    )
    fatigue: parts_fatigue.FatigueTracker = pydantic.Field(
        default_factory=parts_fatigue.FatigueTracker
    )
    traits: list[parts_traits.PersonalityTrait]
    abilities: list[parts_ability.Ability]
    flaws: list[parts_aspect.Flaw]
    virtues: list[parts_aspect.Virtue]
    biographic_info: parts_biographic_info.BiographicInfo = pydantic.Field(
        default_factory=parts_biographic_info.BiographicInfo
    )
    reputations: list[parts_rep.Reputation]
    size: Annotated[int, pydantic.Field()] = 0

    @abc.abstractmethod
    def take_damage(self, damage: int) -> None:
        """Take some amount of damage and add an appropriate wound"""
        raise NotImplementedError

    @abc.abstractmethod
    def recover(
        self, duration: datetime.timedelta, recovery_roll: Optional[int] = None
    ) -> None:
        """Take some amount of time and make recovery rolls for corresponding wounds"""
        raise NotImplementedError
