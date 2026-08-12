from app.models.schemas import BirthdayProfile


VALID_THEMES = {
    "iconic_call",
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


def normalize_profile(p: BirthdayProfile) -> BirthdayProfile:

    p.name = p.name.strip()

    p.relationship = p.relationship.strip()

    p.personality = list(
        dict.fromkeys(
            x.strip()
            for x in p.personality
            if x.strip()
        )
    )

    p.interests = list(
        dict.fromkeys(
            x.strip()
            for x in p.interests
            if x.strip()
        )
    )

    if p.theme not in VALID_THEMES:
        p.theme = "iconic_call"

    if p.intensity not in VALID_INTENSITIES:
        p.intensity = "crazy"

    if p.favorite_person:
        p.favorite_person = p.favorite_person.strip()

    return p