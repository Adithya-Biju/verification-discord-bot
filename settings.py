import os
from dotenv import load_dotenv
import pathlib
from logging.config import dictConfig
import logging

logger = logging.getLogger("bot")

load_dotenv()

WEBHOOK_API_KEY = os.getenv("WEBHOOK_API_KEY")
X_API_KEY = os.getenv("X-API-KEY")
DISCORD_API_SECRET = os.getenv("DISCORD_TOKEN")
STANDARD_KEYS = os.getenv("STANDARD_KEYS")
PREMIUM_KEY = os.getenv("PREMIUM_KEY")
APPLICATION_ID = os.getenv("APPLICATION_ID")
MONGO_DB = os.getenv("MONGO_DB")
API_BASE = os.getenv("API_BASE")
API_USSERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")
GUILD_ID = os.getenv("GUILD_ID")
LOGGING_ID = os.getenv("LOGGING_ID")
POSTGRES = os.getenv("POSTGRES")
MONGO_DB_SOFTWARE = os.getenv("MONGO_DB_SOFTWARE")

BASE_DIR = pathlib.Path(__file__).parent
COGS_DIR = BASE_DIR / "cogs"
MODELS_DIR = BASE_DIR / "models"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard": {"format": "%(levelname)-10s - %(name)-15s : %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "console2": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/infos.log",
            "maxBytes": 5_000_000,   # Rotate at 5 MB
            "backupCount": 3,        # Keep 3 backup logs
            "formatter": "verbose",
        },
    },
    "loggers": {
        "bot": {"handlers": ["console", "file"], "level": "INFO", "propagate": False},
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

dictConfig(LOGGING_CONFIG)
