
import json
import sys

from app import config, db


def main():
    checks = {}

    # Check 1: baseline exists and includes three agents.
    try:
        with open(config.BASELINE_PATH, "r", encoding="utf-8") as file:
            baseline = json.load(file)

        checks["baseline"] = (
            len(baseline) == 3
            and all(
                baseline[agent].get("event_count", 0) > 0
                for agent in baseline
            )
        )
    except (FileNotFoundError, json.JSONDecodeError, AttributeError):
        checks["baseline"] = False

    # Check 2: database initializes and returns valid statistics.
    try:
        db.init()
        stats = db.stats()
        checks["database"] = (
            isinstance(stats.get("events_total"), int)
            and isinstance(stats.get("alerts_total"), int)
        )
    except Exception:
        checks["database"] = False

    for name, passed in checks.items():
        print(f"{name}: {'PASS' if passed else 'FAIL'}")

    if not all(checks.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
