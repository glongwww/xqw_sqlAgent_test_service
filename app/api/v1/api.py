from fastapi import APIRouter
from app.api.v1.endpoints import workflow

api_router = APIRouter()
api_router.include_router(workflow.router, prefix="/workflow", tags=["workflow"])
