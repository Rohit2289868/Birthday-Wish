from fastapi import APIRouter, HTTPException
from fastapi.responses import (
    HTMLResponse,
    FileResponse,
)

from app.models.schemas import BirthdayProfile
from app.services.profile_service import (
    normalize_profile,
)
from app.services.llm_service import (
    generate_experience_plan,
)
from app.services.render_service import (
    render_experience,
)
from app.services.experience_store import (
    create_experience,
    get_experience_path,
)


router = APIRouter(
    prefix="/api/birthday",
    tags=["birthday"],
)


@router.post("/generate")
def generate(profile: BirthdayProfile):

    profile = normalize_profile(profile)

    plan = generate_experience_plan(
        profile
    )

    html = render_experience(plan)

    experience_id = create_experience(
        html=html,
        name=profile.name,
    )

    return {
        "experience_id": experience_id,

        "recipient_name": profile.name,

        "preview_url": (
            f"/api/birthday/"
            f"{experience_id}"
        ),

        "download_url": (
            f"/api/birthday/"
            f"{experience_id}/download"
        ),
    }


@router.get(
    "/{experience_id}",
    response_class=HTMLResponse,
)
def preview(experience_id: str):

    try:

        path = get_experience_path(
            experience_id
        )

    except FileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Birthday experience not found.",
        )

    return HTMLResponse(
        path.read_text(
            encoding="utf-8"
        )
    )


@router.get(
    "/{experience_id}/download"
)
def download(experience_id: str):

    try:

        path = get_experience_path(
            experience_id
        )

    except FileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Birthday experience not found.",
        )

    return FileResponse(
        path=path,
        media_type="text/html",
        filename=(
            f"birthday-{experience_id}.html"
        ),
        headers={
            "Content-Disposition":
                f'attachment; '
                f'filename="birthday-{experience_id}.html"'
        },
    )