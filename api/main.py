from fastapi import FastAPI
from settings import logger
from .routes.subscription_status_routes import router as exm_webhook
from .routes.health_routes import router as heatlh
from settings import CORS_PROD, CORS_TEST
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

origin = [
    CORS_TEST,CORS_PROD
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origin,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_credentials=True
)

app.include_router(exm_webhook)
app.include_router(heatlh)