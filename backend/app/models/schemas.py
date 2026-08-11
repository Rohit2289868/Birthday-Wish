from typing import List, Optional

from pydantic import BaseModel, Field


class BirthdayProfile(BaseModel):
    """
    Raw information collected from the person creating
    the birthday experience.
    """

    name: str = Field(min_length=1, max_length=80)
    age: Optional[int] = Field(None, ge=1, le=120)
    gender: Optional[str] = None
    location: Optional[str] = None

    relationship: str = Field(min_length=1, max_length=60)
    known_since: Optional[str] = None
    how_met: Optional[str] = None

    personality: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)

    favorite_person: Optional[str] = None
    favorite_movie_genre: Optional[str] = None

    memorable_story: Optional[str] = None
    funny_fact: Optional[str] = None
    achievement: Optional[str] = None

    private_note: Optional[str] = None
    birthday_message: Optional[str] = None

    theme: str = "surprise"
    intensity: str = "crazy"