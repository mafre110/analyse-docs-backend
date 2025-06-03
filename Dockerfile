FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y libglib2.0-0 libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY backend/app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app /app

ENV PORT=5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "-w", "2"]
