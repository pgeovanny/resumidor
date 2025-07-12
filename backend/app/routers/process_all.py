from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import FileResponse
import os, uuid, tempfile
from app.services.pdf_extractor import extract_text_from_pdf, extract_questions_from_pdf
from app.services.openrouter_api import ask_openrouter, organize_questions_with_ia
import markdown2
import pdfkit

router = APIRouter(prefix="/process-all", tags=["Processamento Automático"])

@router.post("/")
async def process_all(
    lei_pdf: UploadFile = File(...),
    questoes_pdf: UploadFile = File(...),
    modelo_ia: str = Form("mistralai/mixtral-8x7b-instruct"),
    tipo_saida: str = Form("resumo")  # ou "esquematizacao"
):
    # Salva arquivos temporários
    tmp_dir = tempfile.mkdtemp()
    lei_path = os.path.join(tmp_dir, lei_pdf.filename)
    questoes_path = os.path.join(tmp_dir, questoes_pdf.filename)
    with open(lei_path, "wb") as f:
        f.write(await lei_pdf.read())
    with open(questoes_path, "wb") as f:
        f.write(await questoes_pdf.read())

    # Extrai texto e questões
    texto_lei = extract_text_from_pdf(lei_path)
    questoes = extract_questions_from_pdf(questoes_path)

    # Limita a 50 questões para evitar prompts grandes e garantir organização pela IA
    questoes = questoes[:50]

    texto_questoes_brutas = "\n".join(questoes)

    # ETAPA NOVA: ORGANIZAR QUESTÕES VIA IA
    questoes_organizadas = organize_questions_with_ia(texto_questoes_brutas, model=modelo_ia)

    # Prompt IA: analisa padrão da banca com as questões organizadas
    prompt_analise = (
        f"Analise as questões abaixo e explique o que elas cobram, o nível de dificuldade e o padrão da banca:\n{questoes_organizadas}"
    )
    padrao_banca = ask_openrouter(prompt_analise, model=modelo_ia)

    # Prompt IA: gera resumo ou esquematização
    if tipo_saida == "resumo":
        prompt_saida = (
            f"Com base no padrão de cobrança da banca: {padrao_banca}\n"
            f"Faça um resumo didático da lei abaixo, focando nos tópicos mais cobrados, com exemplos e quadros em Markdown. Lei:\n{texto_lei}"
        )
    else:
        prompt_saida = (
            f"Com base no padrão de cobrança da banca: {padrao_banca}\n"
            f"Esquematize visualmente a lei abaixo, usando quadros, fluxogramas, tabelas, tópicos em Markdown. Lei:\n{texto_lei}"
        )
    resultado_markdown = ask_openrouter(prompt_saida, model=modelo_ia)

    # Converte Markdown para HTML e PDF
    html = markdown2.markdown(resultado_markdown)
    output_pdf = os.path.join(tmp_dir, f"resultado_{uuid.uuid4().hex}.pdf")
    pdfkit.from_string(html, output_pdf)

    # Retorna o PDF pronto para download
    return FileResponse(output_pdf, filename="Resumo_Gabarite.pdf", media_type="application/pdf")
