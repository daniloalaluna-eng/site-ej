import csv
import os
from datetime import datetime
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

ARQUIVO_LEADS = "leads.csv"

def salvar_lead(nome: str, email: str, telefone: str, servico: str, mensagem: str):
    arquivo_existe = os.path.isfile(ARQUIVO_LEADS)
    with open(ARQUIVO_LEADS, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not arquivo_existe:
            writer.writerow(["Data/Hora", "Nome", "E-mail", "Telefone", "Servico", "Mensagem"])
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        writer.writerow([data_hora, nome, email, telefone, servico, mensagem])

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/servicos", response_class=HTMLResponse)
def pagina_servicos(request: Request):
    return templates.TemplateResponse(request=request, name="servicos.html")

@app.get("/sobre", response_class=HTMLResponse)
def pagina_sobre(request: Request):
    return templates.TemplateResponse(request=request, name="sobre.html")

@app.get("/contato", response_class=HTMLResponse)
def pagina_contato(request: Request):
    return templates.TemplateResponse(request=request, name="contato.html", context={"sucesso": False})

@app.post("/contato", response_class=HTMLResponse)
def receber_contato(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    servico: str = Form("Geral"),
    mensagem: str = Form(...)
):
    salvar_lead(nome, email, telefone, servico, mensagem)
    print(f"✅ Lead registrado: {nome} | {servico} | {email}")
    return templates.TemplateResponse(
        request=request,
        name="contato.html",
        context={"sucesso": True, "nome_cliente": nome}
    )