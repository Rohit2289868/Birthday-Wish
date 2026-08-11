from app.models.schemas import BirthdayProfile


VALID_THEMES = {
    "cricket",
    "mystery",
    "cinema",
    "gaming",
    "emotional",
    "surprise",
}

VALID_INTENSITIES = {
    "simple",
    "creative",
    "crazy",
    "insane",
}


def clean_list(values: list[str]) -> list[str]:
    """
    Clean strings and remove duplicates
    while preserving order.
    """

    return list(
        dict.fromkeys(
            value.strip()
            for value in values
            if value and value.strip()
        )
    )


def normalize_profile(
    profile: BirthdayProfile,
) -> BirthdayProfile:

    profile.name = profile.name.strip()

    profile.relationship = profile.relationship.strip()

    profile.personality = clean_list(
        profile.personality
    )

    profile.interests = clean_list(
        profile.interests
    )

    if profile.theme not in VALID_THEMES:
        profile.theme = "surprise"

    if profile.intensity not in VALID_INTENSITIES:
        profile.intensity = "crazy"

    return profile