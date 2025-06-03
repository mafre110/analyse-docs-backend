from fastapi import APIRouter, UploadFile, File, HTTPException
import openai, os, fitz, docx2txt, tempfile, shutil

router = APIRouter()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extraire_texte(path: str) -> str:
    if path.endswith(".pdf"):
        txt = ""
        with fitz.open(path) as doc:
            for p in doc: txt += p.get_text()
        return txt
    if path.endswith(".docx"):
        return docx2txt.process(path)
    if path.endswith(".txt"):
        return open(path, encoding="utf-8").read()
    return ""

@router.post("/analyse")
async def analyser(fichier: UploadFile = File(...)):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=fichier.filename)
    shutil.copyfileobj(fichier.file, tmp)
    texte = extraire_texte(tmp.name)
    if not texte.strip():
        raise HTTPException(400, "Extraction vide")

    prompt = f"""
1. Domaine ? 2. Complexité ? 3. Caractéristiques linguistiques.
4. 10 termes + traduction fr-CA.\n\nTexte :\n{texte}
"""
    rep = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2, max_tokens=1000)
    return {"analyse": rep.choices[0].message.content}
