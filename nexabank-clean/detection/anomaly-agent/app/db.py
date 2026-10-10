
import json
import sqlite3
from contextlib import contextmanager

from app import config


@contextmanager
def get_connection():
    connection = sqlite3.connect(config.DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def init():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_time TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                event_json TEXT NOT NULL
            )
        """)
        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_events_agent_time
            ON events(agent_id, event_time)
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                agent_id TEXT,
                alert_json TEXT NOT NULL
            )
        """)


def insert_event(event):
    payload = (
        event.model_dump(mode="json")
        if hasattr(event, "model_dump")
        else event
    )
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO events (event_time, agent_id, event_json)
            VALUES (?, ?, ?)
            """,
            (
                payload["event_time"],
                payload["agent_id"],
                json.dumps(payload),
            ),
        )
        return cursor.lastrowid


def insert_alert(alert):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO alerts
                (created_at, alert_type, severity, agent_id, alert_json)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                alert.get("created_at", ""),
                alert.get("type", "unknown"),
                alert.get("severity", "low"),
                alert.get("agent_id"),
                json.dumps(alert),
            ),
        )
        return cursor.lastrowid


def stats():
    with get_connection() as connection:
        events_total = connection.execute(
            "SELECT COUNT(*) FROM events"
        ).fetchone()[0]

        alerts_total = connection.execute(
            "SELECT COUNT(*) FROM alerts"
        ).fetchone()[0]

        last_event = connection.execute(
            "SELECT MAX(event_time) FROM events"
        ).fetchone()[0]

    return {
        "events_total": events_total,
        "alerts_total": alerts_total,
        "last_event_time": last_event,
    }
