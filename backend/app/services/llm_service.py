import json
import os

from dotenv import load_dotenv
from google import genai

from app.models.schemas import (
    BirthdayProfile,
    ExperiencePlan,
)


load_dotenv()


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)


if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured."
    )


client = genai.Client(
    api_key=GEMINI_API_KEY
)


SYSTEM_INSTRUCTION = """
You are the creative AI engine behind a
premium personalized birthday experience.

Your job is NOT to generate HTML.

Your job is to transform the birthday
recipient's information into a structured
ExperiencePlan.

The ExperiencePlan will later be rendered
into HTML by our application.

Rules:

1. Never invent personal facts.
2. Only use information provided by the user.
3. You may creatively phrase provided facts.
4. The tone should feel personal, funny,
   playful and emotionally warm.
5. Avoid generic birthday wishes.
6. Create memorable storytelling.
7. Use the recipient's interests naturally.
8. Keep the experience entertaining.
9. Do not claim that a real celebrity has
   endorsed, called, or personally contacted
   the recipient.
10. If the user mentions a celebrity, treat
    that as a fan-theme or fictional tribute,
    not a real endorsement.
11. Return ONLY valid JSON.
12. The JSON must match the requested schema.
"""


def build_prompt(
    profile: BirthdayProfile,
) -> str:

    profile_data = profile.model_dump(
        exclude_none=True
    )

    return f"""
Create a personalized birthday experience
for the following person.

PERSON INFORMATION:

{json.dumps(
    profile_data,
    indent=2,
    ensure_ascii=False
)}

Create content that feels like it was written
by a close friend who knows this person.

The experience should have:

- A strong hero section
- A friendship timeline
- Interesting statistics
- A funny but friendly roast
- A surprise/reveal section
- A memorable final birthday message

Use the person's hobbies, education,
career, friendship history and personality
where available.

Do not invent missing information.

Return ONLY JSON matching the
ExperiencePlan schema.
"""


def generate_experience_plan(
    profile: BirthdayProfile,
) -> ExperiencePlan:

    prompt = build_prompt(profile)

    response = client.models.generate_content(
        model=GEMINI_MODEL,

        contents=prompt,

        config={
            "system_instruction":
                SYSTEM_INSTRUCTION,

            "response_mime_type":
                "application/json",

            "response_schema":
                ExperiencePlan,
        },
    )


    if not response.text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )


    try:

        data = json.loads(
            response.text
        )

    except json.JSONDecodeError as exc:

        raise RuntimeError(
            "Gemini returned invalid JSON."
        ) from exc


    try:

        return ExperiencePlan.model_validate(
            data
        )

    except Exception as exc:

        raise RuntimeError(
            "Gemini response does not match "
            "ExperiencePlan schema."
        ) from exc