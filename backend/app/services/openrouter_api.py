import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

def ask_openrouter(prompt: str, model: str = "mistralai/mixtral-8x7b-instruct") -> str:
    if not OPENROUTER_API_KEY:
        return "OpenRouter API Key não configurada."
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Gabarite App"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Você é um especialista em provas de concurso e legislação."},
            {"role": "user", "content": prompt}
        ]
    }
    r = requests.post(url, json=payload, headers=headers, timeout=90)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("ERRO DA OPENROUTER:", r.text)
        raise
    return r.json()["choices"][0]["message"]["content"]

def organize_questions_with_ia(raw_questions: str, model: str = "mistralai/mixtral-8x7b-instruct") -> str:
    prompt = (
        "O texto a seguir contém várias questões de concurso extraídas de um PDF, mas está desorganizado, podendo estar sem numeração, com alternativas misturadas ou gabaritos juntos do enunciado.\n"
        "Organize essas questões da seguinte forma:\n"
        "- Separe cada questão com número.\n"
        "- Destaque o enunciado.\n"
        "- Separe claramente as alternativas (A, B, C, D, E).\n"
        "- Se o gabarito estiver junto, destaque ao final da questão como 'Gabarito: ___'.\n"
        "- Corrija possíveis misturas e torne todas as questões fáceis de ler e prontas para análise.\n\n"
        f"Texto das questões extraídas:\n{raw_questions}"
    )
    return ask_openrouter(prompt, model=model)
