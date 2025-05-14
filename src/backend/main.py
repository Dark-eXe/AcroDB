from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse
from backend.api.routes import router
from backend.core.config import CORS_CONFIG
from backend.core.rate_limit import limiter

app = FastAPI()

# Setup slowapi
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda request, exc: JSONResponse(
    status_code=429,
    content={"error": "Rate limit exceeded. Try again soon."}
))
app.add_middleware(SlowAPIMiddleware)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    **CORS_CONFIG
)

# Include routes
app.include_router(router)
