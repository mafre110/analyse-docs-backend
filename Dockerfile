# -------- IMAGE DE BASE MINIMALE --------
FROM python:3.10-slim

# PyMuPDF a besoin de quelques librairies système
RUN apt-get update && \
    apt-get install -y libglib2.0-0 libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

# -------- VARIABLES D’ENVIRONNEMENT --------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000   # Azure Container Apps lira ce port

# -------- DÉPENDANCES PYTHON --------
WORKDIR /app
COPY backend/app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# -------- COPIE DU CODE --------
COPY backend/app /app

# -------- COMMAND START --------
# lance l'appli Flask en production avec gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:app"]
