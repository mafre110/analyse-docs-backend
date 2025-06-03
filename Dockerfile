FROM python:3.10-slim

# Dépendances système pour PyMuPDF
RUN apt-get update && \
    apt-get install -y libglib2.0-0 libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PORT=10000

CMD gunicorn app:app -w 2 -b 0.0.0.0:$PORT
