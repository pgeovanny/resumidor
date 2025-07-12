from fastapi import APIRouter, Body
from app.services.deepseek_api import ask_deepseek

router = APIRouter(prefix="/deepseek", tags=["DeepSeek"])

@router.post("/ask")
def ask_ia(prompt: str = Body(..., embed=True)):
    response = ask_deepseek(prompt)
    return {"response": response}
