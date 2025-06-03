# Analyse Docs Backend (Render Edition)

Service FastAPI conteneurisé pour analyser automatiquement des documents (PDF, DOCX, TXT) avec GPT‑4.

## Déploiement en 3 minutes sur Render

1. **Fork** ou clonez ce dépôt sur GitHub.
2. Créez un compte sur [Render](https://render.com) et connectez votre GitHub.
3. Dashboard Render → **+ New → Web Service**
   - Sélectionnez le dépôt **analyse-docs-backend-render**  
   - Type = **Docker** (Render détecte le Dockerfile)  
   - Plan = *Free* ou *Starter*  
4. Dans **Environment › Environment Variables**, ajoutez :
   - `OPENAI_API_KEY` = *votre clé secrète OpenAI*
5. Cliquez **Create Web Service**.  
   Render construit l’image puis publie votre API sur  
   `https://analyse-docs.onrender.com`.

## Endpoint

```
POST /analyser
Form‑data : fichier=<PDF|DOCX|TXT>
```

La réponse JSON contient :
- domaine,
- complexité,
- caractéristiques linguistiques,
- tableau terminologique bilingue.

## Test local

```bash
docker build -t analyse:test .
docker run -p 5000:10000 analyse:test
curl -X POST http://localhost:5000/analyser -F "fichier=@mon.pdf"
```
