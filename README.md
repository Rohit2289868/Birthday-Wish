# Wishcraft — Birthday Experience Generator

Modular MVP: responsive frontend → FastAPI → normalized birthday profile → structured experience plan → Jinja2 renderer → personalized HTML.

The LLM boundary lives in `backend/app/services/llm_service.py`. It currently contains a deterministic mock so the project runs without an API key. Replace that function with an LLM call that returns the `ExperiencePlan` schema; do not ask the LLM to generate raw HTML.

## Run

Backend:
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `frontend/index.html` through a local static server. The frontend expects FastAPI at `http://127.0.0.1:8000`.
