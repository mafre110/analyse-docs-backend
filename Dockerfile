FROM python:3.10-slim

# Bibliothèques système nécessaires à PyMuPDF
RUN apt-get update && \
    apt-get install -y libglib2.0-0 libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Variables d’environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5000               # Port écouté par Flask dans app.py

# Dépendances Python
COPY backend/app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code applicatif
COPY backend/app /app

# Démarrage de l’application (2 workers Gunicorn)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "-w", "2"]
