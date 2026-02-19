from fastapi import APIRouter

from app.api.v1.endpoints import conversations, debtors, metrics, ws

api_router = APIRouter()

api_router.include_router(debtors.router, prefix="/debtors", tags=["debtors"])
api_router.include_router(
    conversations.router, prefix="/conversations", tags=["conversations"]
)
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
api_router.include_router(ws.router, prefix="/ws", tags=["websocket"])
