from fastapi import FastAPI
from app.api.routes import router as task_router
from app.api.metrics_routes import router as metrics_router

app = FastAPI(title="Agentic AI System")

app.include_router(task_router)
app.include_router(metrics_router)
