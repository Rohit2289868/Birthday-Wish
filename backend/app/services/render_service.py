from pathlib import Path

from jinja2 import (
    Environment,
    FileSystemLoader,
    select_autoescape,
)

from app.models.experience import ExperiencePlan


BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATE_DIR = BASE_DIR / "templates"


env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(
        ["html", "xml"]
    ),
)


def render_experience(
    plan: ExperiencePlan,
) -> str:

    template = env.get_template(
        "birthday.html"
    )

    return template.render(
        plan=plan.model_dump()
    )