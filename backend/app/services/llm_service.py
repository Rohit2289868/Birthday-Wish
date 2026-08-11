from uuid import uuid4

from app.models.schemas import BirthdayProfile

from app.models.experience import (
    ExperiencePlan,
    ExperienceMeta,
    HeroSection,
    TimelineSection,
    TimelineItem,
    StatsSection,
    Stat,
    TextSection,
    SurpriseSection,
    Theme,
)


def pick_theme(
    profile: BirthdayProfile,
) -> Theme:

    if profile.theme != "surprise":

        return Theme(profile.theme)

    interests = " ".join(
        profile.interests
    ).lower()

    if "cricket" in interests:

        return Theme.CRICKET

    if "movie" in interests:

        return Theme.CINEMA

    if "gaming" in interests:

        return Theme.GAMING

    return Theme.CELEBRATION


def generate_experience_plan(
    profile: BirthdayProfile,
) -> ExperiencePlan:

    """
    Temporary creative engine.

    Later this function will call the LLM.

    The important part is that the LLM will return
    an ExperiencePlan instead of raw HTML.
    """

    theme = pick_theme(profile)

    name = profile.name

    personality = (
        ", ".join(profile.personality[:3])
        if profile.personality
        else "one-of-a-kind"
    )

    interest = (
        profile.interests[0]
        if profile.interests
        else "good times"
    )

    # -----------------------------------------------------
    # HERO
    # -----------------------------------------------------

    if theme == Theme.CRICKET:

        hero = HeroSection(
            eyebrow="SPECIAL DELIVERY // BIRTHDAY MATCH",
            title=name.upper(),
            subtitle=(
                f"{personality.title()} • "
                f"{interest.title()} • "
                "Main-character energy"
            ),
            badge="🏏 CRICKET LEGEND",
            cta={
                "label": "START THE EXPERIENCE",
                "action": "scroll",
            },
        )

        roast = TextSection(
            type="roast",
            eyebrow="OFFICIAL SCOUTING REPORT",
            title="The birthday roast.",
            body=(
                profile.funny_fact
                or (
                    f"Scouting report: {name} "
                    f"takes {interest} way too seriously."
                )
            ),
            icon="🏏",
        )

        surprise = SurpriseSection(
            title="📞 THE CALL-UP",
            body=(
                f"Incoming birthday protocol for "
                f"{name}. Answer the call and "
                "unlock the surprise."
            ),
            interaction="reveal",
        )

    elif theme == Theme.MYSTERY:

        hero = HeroSection(
            eyebrow="CLASSIFIED // BIRTHDAY CASE",
            title=f"CASE: {name.upper()}",
            subtitle=(
                "A suspiciously good birthday "
                "has been detected."
            ),
            badge="🕵️ CASE FILE",
            cta={
                "label": "OPEN CASE",
                "action": "scroll",
            },
        )

        roast = TextSection(
            type="roast",
            eyebrow="DETECTIVE'S NOTE",
            title="The suspect profile.",
            body=(
                profile.funny_fact
                or (
                    f"{name} has been caught "
                    f"being {personality}."
                )
            ),
            icon="🕵️",
        )

        surprise = SurpriseSection(
            title="🔐 THE FINAL CLUE",
            body=(
                "One last classified file "
                "contains the message they "
                "were never expecting."
            ),
            interaction="reveal",
        )

    else:

        hero = HeroSection(
            eyebrow="A SPECIAL PRODUCTION // TODAY",
            title=name.upper(),
            subtitle=(
                "One person. One story. "
                "One unforgettable birthday."
            ),
            badge="✨ PERSONALIZED EXPERIENCE",
            cta={
                "label": "BEGIN",
                "action": "scroll",
            },
        )

        roast = TextSection(
            type="roast",
            eyebrow="OFFICIAL REPORT",
            title="Things we love about them.",
            body=(
                profile.funny_fact
                or (
                    f"Official diagnosis: "
                    f"{name} is {personality}."
                )
            ),
            icon="✨",
        )

        surprise = SurpriseSection(
            title="✨ THE SURPRISE",
            body=(
                f"The birthday experience "
                f"is ready for {name}."
            ),
            interaction="reveal",
        )

    # -----------------------------------------------------
    # TIMELINE
    # -----------------------------------------------------

    timeline = TimelineSection(
        title="Every friendship has chapters.",
        subtitle="The story so far.",
        items=[
            TimelineItem(
                label="01",
                title="HOW IT STARTED",
                description=(
                    profile.how_met
                    or (
                        "That is where the "
                        f"{profile.relationship.lower()} "
                        "story began."
                    )
                ),
                icon="✦",
            ),

            TimelineItem(
                label="02",
                title="THE MEMORIES",
                description=(
                    profile.memorable_story
                    or (
                        "A collection of moments "
                        "that became stories worth "
                        "remembering."
                    )
                ),
                icon="◌",
            ),

            TimelineItem(
                label="03",
                title="THE JOURNEY",
                description=(
                    profile.achievement
                    or (
                        "Another year, another "
                        "chapter, another reason "
                        "to celebrate."
                    )
                ),
                icon="↗",
            ),
        ],
    )

    # -----------------------------------------------------
    # STATS
    # -----------------------------------------------------

    stats = StatsSection(
        title="THE NUMBERS",
        stats=[
            Stat(
                value=profile.known_since or "∞",
                label="TIME TOGETHER",
            ),

            Stat(
                value=str(
                    len(profile.interests)
                ),
                label="OBSESSIONS",
            ),

            Stat(
                value="1",
                label="BIRTHDAY LEGEND",
            ),
        ],
    )

    # -----------------------------------------------------
    # FINAL MESSAGE
    # -----------------------------------------------------

    final_message = TextSection(
        type="final",
        eyebrow="FINAL MESSAGE",
        title=f"HAPPY BIRTHDAY, {name}.",
        body=(
            profile.birthday_message
            or (
                f"Happy Birthday, {name}! "
                "Keep being exactly the kind "
                "of person people are lucky to "
                "have in their lives. Here's to "
                "bigger dreams, louder laughs "
                "and an incredible year ahead."
            )
        ),
    )

    # -----------------------------------------------------
    # EXPERIENCE PLAN
    # -----------------------------------------------------

    plan = ExperiencePlan(

        meta=ExperienceMeta(
            experience_id=str(uuid4()),
            recipient_name=name,
            theme=theme,
            tone="funny-playful",
            intensity=profile.intensity,
        ),

        hero=hero,

        sections=[
            timeline.model_dump(),
            stats.model_dump(),
            roast.model_dump(),
            surprise.model_dump(),
        ],

        final_message=final_message,

        safety_notes=[
            (
                "Do not invent private facts "
                "not supplied by the creator."
            ),
            (
                "Do not impersonate a real person "
                "or claim a real celebrity endorsed "
                "the experience."
            ),
        ],
    )

    return plan