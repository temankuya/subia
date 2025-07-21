import logging
import os
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

# Load environment variables from config.env
load_dotenv("config.env")

# Helper: convert string to boolean
def to_bool(value: str) -> bool:
    return value.strip().lower() in ("true", "1", "yes", "y", "on")

# Helper: convert string to int with fallback
def to_int(value: str, default: int = 0) -> int:
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

# === ENV CONFIGURATION ===

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
API_ID = to_int(os.getenv("API_ID", "16460673"))
API_HASH = os.getenv("API_HASH", "cced480d69646bf00285e8e46b6979a8")

CHANNEL_DB = to_int(os.getenv("CHANNEL_DB", "-1002885860312"))
MONGO_URL = os.getenv("MONGO_URL", "")

RESTRICT = to_bool(os.getenv("RESTRICT", "true"))

# Force subscription channels
FORCE_SUB_1 = to_int(os.getenv("FORCE_SUB_1", "0"))
FORCE_SUB_2 = to_int(os.getenv("FORCE_SUB_2", "0"))
FORCE_SUB_3 = to_int(os.getenv("FORCE_SUB_3", "0"))

WORKERS = to_int(os.getenv("WORKERS", "4"))

# Start message
START_MESSAGE = os.getenv(
    "START_MESSAGE",
    (
        "Halo {mention}!\n\n"
        "Saya dapat menyimpan file pribadi di Channel tertentu dan pengguna lain "
        "dapat mengaksesnya dari link khusus."
    ),
)

# Force-sub message
FORCE_MESSAGE = os.getenv(
    "FORCE_MESSAGE",
    (
        "Halo {mention}!\n\n"
        "Anda harus bergabung di Channel/Group terlebih dahulu untuk melihat file "
        "yang saya bagikan.\n\nSilakan Join Ke Channel/Group terlebih dahulu."
    ),
)

# Admins (space-separated user IDs)
try:
    ADMINS = [int(x) for x in os.getenv("ADMINS", "5909047294 1642887477 2096354247").split()]
except ValueError:
    raise ValueError("ADMINS harus berisi daftar User ID yang valid (dipisahkan spasi)")

CUSTOM_CAPTION = os.getenv("CUSTOM_CAPTION", None)
DISABLE_BUTTON = to_bool(os.getenv("DISABLE_BUTTON", "false"))

# === LOGGING SETUP ===

LOGS_FILE = "logs.txt"
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOGS_FILE, maxBytes=50_000_000, backupCount=10),
        logging.StreamHandler(),
    ],
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

LOGGER = get_logger(__name__)
