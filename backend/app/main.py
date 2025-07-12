from fastapi import FastAPI
from app.routers import upload, extract, openrouter, process_all

app = FastAPI(
    title="Gabarite Backend",
    description=(
        "API para upload, extração e análise de leis e questões com IA OpenRouter, "
        "fluxo automatizado de resumo/esquematização e exportação para PDF."
    )
)

app.include_router(upload.router)
app.include_router(extract.router)
app.include_router(openrouter.router)
app.include_router(process_all.router)
