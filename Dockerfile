# Imagem base
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app"

# Dependências de sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# =========================
# 1️⃣ Dependências (cache)
# =========================
COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# =========================
# 2️⃣ Código do projeto
# =========================
COPY . .

# Garante diretórios
RUN mkdir -p data/pdfs data/vectorstore

# Script de start
RUN echo '#!/bin/sh\n\
if [ ! -d "data/vectorstore" ] || [ -z "$(ls -A data/vectorstore 2>/dev/null)" ]; then\n\
  echo "[INFO] Vectorstore vazio. Rodando ingest..."\n\
  python src/ingest.py\n\
fi' > /app/start.sh \
&& chmod +x /app/start.sh


# Comando final
CMD ["bash", "-c", "/app/start.sh && uvicorn api.main:app --host 0.0.0.0 --port 8000"]





