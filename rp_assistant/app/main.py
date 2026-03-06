from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import shutil
import os

from .rag_pipeline import process_pdf, query_paper
from .schemas import Question

app = FastAPI(title="Research Paper Assistant")

UPLOAD_DIR = "data"

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    process_pdf(file_path)

    return {"message": "PDF uploaded successfully"}


@app.post("/ask")
def ask_question(q: Question):

    answer = query_paper(q.question)

    return {"answer": answer}