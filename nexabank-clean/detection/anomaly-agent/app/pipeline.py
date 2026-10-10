
import json

from app import db, config
from app.detectors import detect_event
from app.narrative import generate_narrative
from app.notify import send_alert
from app.schemas import Event
from app.timeutil import iso_utc, now_utc


def load_baseline():
    """Load the trained agent baseline."""
    try:
        with open(config.BASELINE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def process_event(raw_event, baseline=None):
    """Validate and process one transaction event."""
    event = Event.model_validate(raw_event)
    event_data = event.model_dump(mode="json")

    db.init()
    event_id = db.insert_event(event_data)

    if baseline is None:
        baseline = load_baseline()

    alerts = detect_event(event_data, baseline)
    processed_alerts = []

    for alert in alerts:
        narrative = generate_narrative(alert)

        full_alert = {
            **alert,
            "created_at": iso_utc(now_utc()),
            "narrative": narrative,
        }

        db.insert_alert(full_alert)
        full_alert["notification"] = send_alert(full_alert)
        processed_alerts.append(full_alert)

    return {
        "status": "ok",
        "event_id": event_id,
        "alert_count": len(processed_alerts),
        "alerts": processed_alerts,
    }
