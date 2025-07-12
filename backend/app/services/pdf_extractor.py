import pdfplumber
import re

def extract_text_from_pdf(pdf_path: str) -> str:
    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            all_text += page.extract_text() or ""
    return all_text

def extract_questions_from_pdf(pdf_path: str) -> list:
    text = extract_text_from_pdf(pdf_path)
    # Expressão para separar questões numeradas (1., 2., 3., ...)
    # Ajuste conforme o padrão do seu PDF!
    question_blocks = re.split(r'\n?\s*(?:\d+|[IVXLCDM]+)[\.\)]\s+', text)
    questions = [q.strip() for q in question_blocks if len(q.strip()) > 30]
    return questions
