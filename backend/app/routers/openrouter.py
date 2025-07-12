from fastapi import APIRouter, Body
from app.services.openrouter_api import ask_openrouter

router = APIRouter(prefix="/openrouter", tags=["OpenRouter"])

@router.post("/ask")
def ask_ia(
    prompt: str = Body(..., embed=True),
    model: str = Body("mistralai/mixtral-8x7b-instruct", embed=True)
):
    response = ask_openrouter(prompt, model)
    return {"response": response}
