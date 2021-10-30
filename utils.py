import smtplib
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, Sequence

from flask_caching import Cache

import config


cache: Cache = Cache(
    config={
        "CACHE_TYPE": "filesystem",
        "CACHE_DIR": "/tmp/menu",
    }
)


@dataclass
class Email:
    sender: str
    recipients: Sequence[str]
    subject: str
    body: str
    html: Optional[str] = None


def send_email(
    email: Email,
) -> None:
    _send_email_impl(
        hostname=config.get_mailserver_host(),
        port=config.get_mailserver_port(),
        username=config.get_mailserver_username(),
        password=config.get_mailserver_password(),
        email=email,
    )


def _send_email_impl(
    *,
    hostname: str,
    port: int = 587,
    username: str,
    password: str,
    email: Email,
) -> None:
    message = MIMEMultipart("alternative")
    message["Subject"] = email.subject
    message["From"] = email.sender
    message["To"] = ", ".join(email.recipients)

    message.attach(MIMEText(email.body, "plain", "utf-8"))

    email_html = email.html
    if email_html:
        message.attach(MIMEText(email_html, "html", "utf-8"))

    message = message.as_string()

    if port in (465,):
        server = smtplib.SMTP_SSL(hostname, port)
    else:
        server = smtplib.SMTP(hostname, port)

    server.ehlo()

    if port in (587,):
        server.starttls()

    server.login(username, password)
    server.sendmail(email.sender, email.recipients, message)
    server.close()
    print(f"Sent email to {email.recipients}: {email.subject}")
