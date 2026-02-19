# Agente Voz

Plataforma SaaS B2B de agente conversacional de voz para cobranza inteligente,
basada en PersonaPlex (NVIDIA). Optimiza la recuperacion de cartera vencida
mediante comunicacion empatica, legalmente alineada y emocionalmente adaptativa.

## Stack Tecnico

- **Frontend**: Next.js 14 (App Router) + TypeScript + Tailwind CSS
- **Backend**: Python 3.11 + FastAPI
- **Base de datos**: PostgreSQL + pgvector
- **Cache**: Redis
- **RAG**: LangChain + pgvector
- **STT**: faster-whisper
- **TTS**: Coqui TTS
- **Voice Model**: PersonaPlex (NVIDIA)
- **Audio**: WebRTC + WebSocket
- **Infra**: Docker + Docker Compose

## Estructura del Proyecto

```
agente_voz/
  backend/          # FastAPI + servicios de IA
  frontend/         # Next.js dashboard
  docker-compose.yml
```

## Inicio Rapido

```bash
# Levantar todo el stack
docker compose up --build

# Solo backend
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload

# Solo frontend
cd frontend && npm install && npm run dev
```

## Fases

- **Fase 0**: Investigacion y diseno (actual)
- **Fase 1**: MVP conversacional web
- **Fase 2**: Integracion empresarial
- **Fase 3**: Escalabilidad y diferenciacion IA
- **Fase 4**: Expansion y ecosistema
