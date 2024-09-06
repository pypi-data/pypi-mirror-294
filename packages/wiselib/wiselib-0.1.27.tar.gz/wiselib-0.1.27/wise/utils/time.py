from datetime import datetime
from time import time

from django.utils.timezone import make_aware

ISO_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
ISO_TIME_FORMAT_WITH_MS = "%Y-%m-%dT%H:%M:%S.%f%z"


def iso_serialize(dt: datetime, with_ms: bool = False) -> str:
    return dt.strftime(ISO_TIME_FORMAT_WITH_MS if with_ms else ISO_TIME_FORMAT)


def iso_deserialize(s: str) -> datetime:
    try:
        return datetime.strptime(s, ISO_TIME_FORMAT_WITH_MS)
    except ValueError:
        return datetime.strptime(s, ISO_TIME_FORMAT)


def expire_from_now(*, hours: int = 0, minutes: int = 0):
    return time() + hours * 3600 + minutes * 60


def get_datetime_from_timestamp(ts: int, tz_aware: bool = True) -> datetime:
    dt = datetime.fromtimestamp(ts / 1000)
    return make_aware(dt) if tz_aware else dt


def get_timestamp_from_datetime(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)
