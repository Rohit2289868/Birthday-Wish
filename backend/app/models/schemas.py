from typing import List, Optional

from pydantic import BaseModel, Field


class BirthdayProfile(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=80
    )

    age: Optional[int] = Field(
        None,
        ge=1,
        le=120
    )

    gender: Optional[str] = None
    location: Optional[str] = None

    relationship: str = Field(
        min_length=1,
        max_length=60
    )

    known_since: Optional[str] = None
    how_met: Optional[str] = None

    personality: List[str] = Field(
        default_factory=list
    )

    interests: List[str] = Field(
        default_factory=list
    )

    favorite_person: Optional[str] = None
    favorite_movie_genre: Optional[str] = None

    memorable_story: Optional[str] = None
    funny_fact: Optional[str] = None
    achievement: Optional[str] = None
    private_note: Optional[str] = None
    birthday_message: Optional[str] = None

    # Experience configuration

    theme: str = "iconic_call"

    intensity: str = "crazy"


class TimelineItem(BaseModel):

    number: str

    title: str

    description: str


class CallExperience(BaseModel):

    enabled: bool = False

    # Person the birthday recipient admires.
    favorite_person: Optional[str] = None

    caller_label: str = "SPECIAL CALL"

    call_title: str = "Incoming birthday call"

    message: str = ""

    # Optional authorized/user-provided audio.
    audio_url: Optional[str] = None

    # Keeps the experience from being presented
    # as a real celebrity communication.
    fan_made: bool = True

    disclaimer: str = (
        "Fan-made birthday experience. "
        "This is not an actual call, recording, "
        "endorsement, or communication from "
        "the person referenced."
    )


class ExperiencePlan(BaseModel):

    theme: str

    eyebrow: str

    title: str

    subtitle: str

    timeline: List[TimelineItem]

    roast: str

    achievement: str

    surprise_title: str

    surprise_text: str

    final_message: str

    call: CallExperience = Field(
        default_factory=CallExperience
    )