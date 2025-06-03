# Analyse Docs Backend

Service FastAPI pour analyser automatiquement des documents (PDF, DOCX, TXT) avec GPT‑4 et retourner:
- domaine,
- niveau de complexité,
- caractéristiques linguistiques,
- terminologie spécialisée avec traduction fr‑CA.

## Déploiement rapide

1. Fork/clone ce repo.
2. Renseigner les secrets GitHub indiqués dans `.github/workflows/deploy.yml`.
3. Push sur `main`; GitHub Actions construit l'image et met à jour Azure Container Apps.

## Test local

```bash
docker build -t analyse:test .
docker run -p 5000:5000 analyse:test
curl -X POST http://localhost:5000/analyser -F "fichier=@mon.pdf"
```
