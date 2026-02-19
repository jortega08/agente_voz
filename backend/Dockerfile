FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Instalar torch primero (paquete mas pesado)
RUN pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# Instalar TTS por separado (tambien pesado, ya usa torch instalado)
RUN pip install --no-cache-dir TTS==0.22.0

# Instalar faster-whisper por separado
RUN pip install --no-cache-dir faster-whisper==1.1.0

# Instalar langchain y ML por separado
RUN pip install --no-cache-dir \
    langchain==0.3.14 \
    langchain-community==0.3.14 \
    langchain-huggingface==0.1.2

# Instalar el resto de dependencias
RUN pip install --no-cache-dir \
    fastapi==0.115.6 \
    uvicorn[standard]==0.34.0 \
    pydantic==2.10.4 \
    pydantic-settings==2.7.1 \
    python-dotenv==1.0.1 \
    sqlalchemy[asyncio]==2.0.36 \
    asyncpg==0.30.0 \
    alembic==1.14.1 \
    pgvector==0.3.6 \
    redis[hiredis]==5.2.1 \
    numpy==1.26.4 \
    soundfile==0.12.1 \
    webrtcvad==2.0.10 \
    httpx==0.28.1 \
    websockets==14.1 \
    structlog==24.4.0 \
    pytest==8.3.4 \
    pytest-asyncio==0.25.0

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
