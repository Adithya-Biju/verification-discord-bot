import os
from dotenv import load_dotenv
import pathlib

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

BASE_DIR = pathlib.Path(__file__).parent
COGS_DIR = BASE_DIR / "cogs"

