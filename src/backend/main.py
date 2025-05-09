from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import CORS_CONFIG
from backend.api.routes import router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    **CORS_CONFIG
)

app.include_router(router)