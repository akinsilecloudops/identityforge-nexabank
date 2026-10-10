
import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DATA_DIR = os.getenv("DATA_DIR", "./data")
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "identityforge.db")
BASELINE_PATH = os.path.join(DATA_DIR, "baseline.json")

INGEST_API_KEY = os.getenv("INGEST_API_KEY", "")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

OLLAMA_URL = os.getenv(
    "OLLAMA_URL", "http://localhost:11434"
).rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "90"))

Z_LIMIT = float(os.getenv("Z_LIMIT", "3.0"))
MIN_VOLUME_COUNT = int(os.getenv("MIN_VOLUME_COUNT", "10"))
RARE_HOUR_SHARE = float(os.getenv("RARE_HOUR_SHARE", "0.01"))
MIN_BASELINE_EVENTS = int(os.getenv("MIN_BASELINE_EVENTS", "50"))
ALERT_COOLDOWN_SECONDS = int(
    os.getenv("ALERT_COOLDOWN_SECONDS", "600")
)

TIMEZONE = "Africa/Lagos"
SENTRY_DSN = os.getenv("SENTRY_DSN", "")