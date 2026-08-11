from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------
# THEMES
# ---------------------------------------------------------

class Theme(str, Enum):
    CRICKET = "cricket"
    MYSTERY = "mystery"
    CINEMA = "cinema"
    GAMING = "gaming"
    EMOTIONAL = "emotional"
    CELEBRATION = "celebration"


# ---------------------------------------------------------
# SECTION TYPES
# ---------------------------------------------------------

class SectionType(str, Enum):
    TIMELINE = "timeline"
    STATS = "stats"
    ROAST = "roast"
    ACHIEVEMENT = "achievement"
    GALLERY = "gallery"
    QUOTE = "quote"
    SURPRISE = "surprise"
    AUDIO = "audio"
    FINAL = "final"


# ---------------------------------------------------------
# COMMON
# ---------------------------------------------------------

class CTA(BaseModel):
    label: str
    action: str = "scroll"


class ExperienceMeta(BaseModel):
    experience_id: str
    recipient_name: str

    theme: Theme

    tone: str
    intensity: str

    language: str = "en"


# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------

class HeroSection(BaseModel):
    type: Literal["hero"] = "hero"

    eyebrow: str
    title: str
    subtitle: str

    badge: Optional[str] = None
    cta: Optional[CTA] = None


# ---------------------------------------------------------
# TIMELINE
# ---------------------------------------------------------

class TimelineItem(BaseModel):
    label: Optional[str] = None

    title: str
    description: str

    icon: Optional[str] = None


class TimelineSection(BaseModel):
    type: Literal["timeline"] = "timeline"

    title: str
    subtitle: Optional[str] = None

    items: List[TimelineItem] = Field(
        default_factory=list
    )


# ---------------------------------------------------------
# STATS
# ---------------------------------------------------------

class Stat(BaseModel):
    value: str
    label: str


class StatsSection(BaseModel):
    type: Literal["stats"] = "stats"

    title: Optional[str] = None

    stats: List[Stat] = Field(
        default_factory=list
    )


# ---------------------------------------------------------
# TEXT-BASED SECTIONS
# ---------------------------------------------------------

class TextSection(BaseModel):
    type: SectionType

    eyebrow: Optional[str] = None

    title: str

    body: str

    icon: Optional[str] = None


# ---------------------------------------------------------
# SURPRISE
# ---------------------------------------------------------

class SurpriseSection(BaseModel):
    type: Literal["surprise"] = "surprise"

    title: str

    body: str

    interaction: str = "reveal"


# ---------------------------------------------------------
# MEDIA
# ---------------------------------------------------------

class MediaAsset(BaseModel):
    url: str

    alt: str = ""

    caption: Optional[str] = None


class GallerySection(BaseModel):
    type: Literal["gallery"] = "gallery"

    title: str

    assets: List[MediaAsset] = Field(
        default_factory=list
    )


# ---------------------------------------------------------
# FINAL EXPERIENCE PLAN
# ---------------------------------------------------------

class ExperiencePlan(BaseModel):
    """
    The contract between the AI/creative layer
    and the deterministic rendering layer.

    IMPORTANT:

    The LLM should generate this structure.

    The LLM should NOT generate arbitrary HTML,
    CSS or JavaScript.
    """

    meta: ExperienceMeta

    hero: HeroSection

    sections: List[Dict[str, Any]] = Field(
        default_factory=list
    )

    final_message: TextSection

    safety_notes: List[str] = Field(
        default_factory=list
    )