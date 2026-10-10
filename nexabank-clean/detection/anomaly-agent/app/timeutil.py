
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from app import config

LAGOS = ZoneInfo(config.TIMEZONE)
ISO_FMT = "%Y-%m-%dT%H:%M:%SZ"


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def to_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def iso_utc(dt: datetime) -> str:
    return to_utc(dt).strftime(ISO_FMT)


def to_local(dt: datetime) -> datetime:
    return to_utc(dt).astimezone(LAGOS)


def hour_window(dt: datetime):
    """Start and end (UTC ISO strings) of the Lagos clock hour containing dt."""
    start = (
        to_local(dt)
        .replace(minute=0, second=0, microsecond=0)
        .astimezone(timezone.utc)
    )
    return iso_utc(start), iso_utc(start + timedelta(hours=1))
