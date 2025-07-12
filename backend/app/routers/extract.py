from fastapi import APIRouter, Query
from app.services.pdf_extractor import extract_text_from_pdf, extract_questions_from_pdf

router = APIRouter(prefix="/extract", tags=["Extract"])

@router.get("/pdf")
def extract_pdf_text(path: str = Query(..., description="Path do arquivo PDF")):
    text = extract_text_from_pdf(path)
    return {"text": text}

@router.get("/questions")
def extract_pdf_questions(path: str = Query(..., description="Path do arquivo PDF")):
    questions = extract_questions_from_pdf(path)
    return {"questions": questions}
