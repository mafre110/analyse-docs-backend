
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import openai, os, fitz, docx2txt, tempfile, shutil
from docx import Document

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extraire_texte(path: str) -> str:
    if path.endswith(".pdf"):
        txt = ""
        with fitz.open(path) as doc:
            for p in doc:
                txt += page.get_text()
        return txt
    if path.endswith(".docx"):
        return docx2txt.process(path)
    if path.endswith(".txt"):
        return open(path, encoding="utf-8").read()
    return ""

@app.post("/analyser")
async def analyser(fichier: UploadFile = File(...)):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=fichier.filename)
    shutil.copyfileobj(fichier.file, tmp)
    texte = extraire_texte(tmp.name)
    if not texte.strip():
        raise HTTPException(status_code=400, detail="Impossible d'extraire le texte.")
    prompt = f"Analyse linguistique complète du texte suivant avec terminologie illimitée et traduction fr-CA:\n\n{texte}"
    rep = openai.ChatCompletion.create(model="gpt-4", messages=[{"role":"user","content":prompt}], temperature=0.2, max_tokens=2000).choices[0].message.content
    doc = Document()
    for line in rep.split("\n"):
        doc.add_paragraph(line)
    out = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(out.name)
    return FileResponse(out.name, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename="analyse.docx")
