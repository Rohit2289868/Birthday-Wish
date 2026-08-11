from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.models.schemas import BirthdayProfile
from app.services.profile_service import normalize_profile
from app.services.llm_service import generate_experience_plan
from app.services.render_service import render_experience


router = APIRouter(
    prefix="/api/birthday",
    tags=["birthday"],
)


@router.post("/plan")
def create_plan(profile: BirthdayProfile):

    profile = normalize_profile(profile)

    plan = generate_experience_plan(profile)

    return plan.model_dump()


@router.post(
    "/generate",
    response_class=HTMLResponse,
)
def generate(profile: BirthdayProfile):

    profile = normalize_profile(profile)

    plan = generate_experience_plan(profile)

    html = render_experience(plan)

    return HTMLResponse(html)