import os
from typing import Sequence
from zoneinfo import ZoneInfo

from pyre_extensions import none_throws


def get_mailserver_host() -> str:
    return str(os.getenv("MAILSERVER_HOST"))


def get_mailserver_port() -> int:
    return int(none_throws(os.getenv("MAILSERVER_PORT")))


def get_mailserver_username() -> str:
    return str(os.getenv("MAILSERVER_USERNAME"))


def get_mailserver_password() -> str:
    return str(os.getenv("MAILSERVER_PASSWORD"))


def get_recipients() -> Sequence[str]:
    recipients = str(os.getenv("RECIPIENTS"))
    return recipients.split(",")


def get_timezone() -> ZoneInfo:
    return ZoneInfo(str(os.getenv("TZ", default="America/Chicago")))
