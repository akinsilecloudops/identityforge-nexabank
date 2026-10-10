import os
import sys
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

from app import config


def check(name, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    suffix = f" — {detail}" if detail else ""
    print(f"[{status}] {name}{suffix}")
    return passed


def main():
    load_dotenv(override=True)
    results = []

    results.append(check(
        "INGEST_API_KEY",
        bool(os.getenv("INGEST_API_KEY", "").strip()),
        "configured" if os.getenv("INGEST_API_KEY", "").strip() else "missing in .env",
    ))

    results.append(check(
        "DASHBOARD_PASSWORD",
        bool(os.getenv("DASHBOARD_PASSWORD", "").strip()),
        "configured" if os.getenv("DASHBOARD_PASSWORD", "").strip() else "missing in .env",
    ))

    slack_url = os.getenv("SLACK_WEBHOOK_URL", "").strip()
    slack_valid = (
        urlparse(slack_url).scheme == "https"
        and bool(urlparse(slack_url).netloc)
        and not any(char.isspace() for char in slack_url)
    )
    results.append(check(
        "SLACK_WEBHOOK_URL",
        slack_valid,
        "configured URL" if slack_valid else "missing or invalid",
    ))

    sentry_dsn = os.getenv("SENTRY_DSN", "").strip()
    sentry_valid = not sentry_dsn or (
        urlparse(sentry_dsn).scheme in ("http", "https")
        and bool(urlparse(sentry_dsn).netloc)
    )
    results.append(check(
        "SENTRY_DSN",
        sentry_valid,
        "configured or optional" if sentry_valid else "invalid URL",
    ))

    try:
        response = requests.get(
            config.OLLAMA_URL + "/api/tags",
            timeout=3,
        )
        ollama_ok = response.ok
    except requests.RequestException:
        ollama_ok = False

    results.append(check(
        "Ollama",
        ollama_ok,
        config.OLLAMA_URL if ollama_ok else "not reachable; start Ollama and retry",
    ))

    data_dir_ok = os.path.isdir(config.DATA_DIR) and os.access(config.DATA_DIR, os.W_OK)
    results.append(check(
        "DATA_DIR",
        data_dir_ok,
        config.DATA_DIR,
    ))

    if all(results):
        print("All checks passed.")
        return 0

    print("One or more checks failed. Fix the items above and run this command again.")
    return 1


if __name__ == "__main__":
    sys.exit(main())