from fastapi import APIRouter, Body
from app.services.gemini_api import ask_gemini

router = APIRouter(prefix="/gemini", tags=["Gemini"])

@router.post("/ask")
def ask_ia(prompt: str = Body(..., embed=True)):
    response = ask_gemini(prompt)
    return {"response": response}
