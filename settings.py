import os
from dotenv import load_dotenv
import pathlib
from logging.config import dictConfig
import logging

load_dotenv()

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
STRIPE_KEY = os.getenv("STRIPE_KEY")

BASE_DIR = pathlib.Path(__file__).parent
COGS_DIR = BASE_DIR / "cogs"

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": False,
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
            "class": "logging.FileHandler",
            "filename": "logs/infos.log",
            "mode": "w",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "bot": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
dictConfig(LOGGING_CONFIG)