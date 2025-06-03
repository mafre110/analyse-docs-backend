from fastapi import FastAPI, UploadFile, File, HTTPException
import openai, os, fitz, docx2txt, tempfile, shutil

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ----------- utilitaire d'extraction -----------
def extraire_texte(path: str) -> str:
    if path.endswith(".pdf"):
        txt = ""
        with fitz.open(path) as doc:
            for p in doc:
                txt += p.get_text()
        return txt
    if path.endswith(".docx"):
        return docx2txt.process(path)
    if path.endswith(".txt"):
        return open(path, encoding="utf-8").read()
    return ""

# ----------- endpoint principal -----------
@app.post("/analyse")
async def analyser(fichier: UploadFile = File(...)):
    # 1. sauvegarde temporaire
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=fichier.filename)
    shutil.copyfileobj(fichier.file, tmp)

    # 2. extraction texte
    texte = extraire_texte(tmp.name)
    if not texte.strip():
        raise HTTPException(400, "Impossible d'extraire le texte.")

    # 3. appel OpenAI
    prompt = f"""
1. Indique le domaine principal.
2. Évalue la complexité (élémentaire / intermédiaire / avancé).
3. Décris ton, style, registre, public cible.
4. Liste 10 termes spécialisés + traduction fr-CA.

Texte :
{texte}
"""
    rep = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2, max_tokens=1000,
    )

    return {"analyse": rep.choices[0].message.content}
