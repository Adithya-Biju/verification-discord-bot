from fastapi import FastAPI
from settings import logger
from .routes.subscription_status_routes import router as exm_webhook


app = FastAPI()
_bot = None 


def set_bot(bot_instance):
    global _bot
    _bot = bot_instance
    logger.info("Bot instance successfully injected into FastAPI app.")

app.include_router(exm_webhook)