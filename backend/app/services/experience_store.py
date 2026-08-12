from pathlib import Path
import uuid


BASE_DIR = Path(__file__).resolve().parent.parent.parent

STORAGE_DIR = BASE_DIR / "generated_experiences"

STORAGE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def create_experience(html: str, name: str) -> str:
    """
    Save a generated birthday experience and return its ID.
    """

    experience_id = str(uuid.uuid4())

    safe_name = "".join(
        c for c in name
        if c.isalnum() or c in (" ", "-", "_")
    ).strip()

    safe_name = safe_name.replace(" ", "-").lower()

    if not safe_name:
        safe_name = "birthday"

    file_path = (
        STORAGE_DIR
        / f"{experience_id}.html"
    )

    file_path.write_text(
        html,
        encoding="utf-8",
    )

    return experience_id


def get_experience_path(
    experience_id: str,
) -> Path:

    path = (
        STORAGE_DIR
        / f"{experience_id}.html"
    )

    if not path.exists():
        raise FileNotFoundError(
            "Birthday experience not found."
        )

    return path