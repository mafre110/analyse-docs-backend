
from fastapi import FastAPI, UploadFile, File, HTTPException
import openai, os, fitz, docx2txt, tempfile, shutil

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extraire_texte(path: str) -> str:
    if path.endswith(".pdf"):
        texte = ""
        with fitz.open(path) as doc:
            for page in doc:
                texte += page.get_text()
        return texte
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

    prompt = f"""Tu es un expert linguistique. Voici un texte provenant d’un document professionnel.

1. Détermine le domaine du texte (ex. : juridique, médical, technique, marketing, etc.)
2. Estime le niveau de complexité linguistique : élémentaire, intermédiaire ou avancé.
3. Décris les caractéristiques linguistiques (ton, style, registre, public cible).
4. Extrait les 10 termes les plus spécifiques au sujet et propose leur traduction en français canadien.

Présente ta réponse sous cette structure :
Domaine : ...
Complexité : ...
Caractéristiques : ...

| Terme anglais | Traduction française |
|---------------|----------------------|

Texte :
{texte}
"""

    rep = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1000,
    )
    return {"analyse": rep.choices[0].message.content}
