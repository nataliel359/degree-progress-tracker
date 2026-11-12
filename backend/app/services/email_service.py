import os
import smtplib
import ssl
from email.message import EmailMessage
from html import escape
from pathlib import Path
from typing import Dict
from urllib.parse import urlencode, urljoin, urlsplit

from dotenv import load_dotenv
from email_validator import validate_email


class EmailConfigurationError(RuntimeError):
    """Raised when required SMTP or frontend configuration is missing or invalid."""


def _load_settings() -> Dict[str, str]:
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")

    required_settings = (
        "FRONTEND_URL",
        "SMTP_HOST",
        "SMTP_PORT",
        "SMTP_USERNAME",
        "SMTP_PASSWORD",
        "SMTP_FROM_EMAIL",
    )
    settings: Dict[str, str] = {}
    for key in required_settings:
        raw_value = os.getenv(key, "")
        trimmed_value = raw_value.strip()
        if not trimmed_value or (
            trimmed_value.startswith("<") and trimmed_value.endswith(">")
        ):
            raise EmailConfigurationError(
                f"{key} must be configured before sending password reset emails."
            )
        settings[key] = (
            raw_value if key in {"SMTP_USERNAME", "SMTP_PASSWORD"} else trimmed_value
        )

    frontend = urlsplit(settings["FRONTEND_URL"])
    if frontend.scheme not in {"http", "https"} or not frontend.netloc:
        raise EmailConfigurationError(
            "FRONTEND_URL must be an absolute HTTP or HTTPS URL."
        )

    try:
        port = int(settings["SMTP_PORT"])
    except ValueError as error:
        raise EmailConfigurationError("SMTP_PORT must be an integer.") from error
    if not 1 <= port <= 65535:
        raise EmailConfigurationError("SMTP_PORT must be between 1 and 65535.")

    return settings


def _validated_email(address: str, setting_name: str) -> str:
    try:
        return validate_email(address, check_deliverability=False).normalized
    except (TypeError, ValueError) as error:
        raise EmailConfigurationError(
            f"{setting_name} must be a valid email address."
        ) from error


def send_password_reset_email(email: str, reset_token: str) -> None:
    """Send a password reset link via authenticated SMTP with STARTTLS."""
    if not isinstance(reset_token, str) or not reset_token.strip():
        raise ValueError("reset_token must be a non-empty string.")

    settings = _load_settings()
    recipient = _validated_email(email, "Recipient email")
    sender = _validated_email(settings["SMTP_FROM_EMAIL"], "SMTP_FROM_EMAIL")

    reset_url = urljoin(
        settings["FRONTEND_URL"].rstrip("/") + "/",
        "reset-password",
    )
    reset_url = f"{reset_url}?{urlencode({'token': reset_token})}"

    message = EmailMessage()
    message["Subject"] = "Reset your Degree Progress Tracker password"
    message["From"] = sender
    message["To"] = recipient
    message.set_content(
        "We received a request to reset your password.\n\n"
        f"Use this link to choose a new password:\n{reset_url}\n\n"
        "If you did not request this, you can ignore this email."
    )
    message.add_alternative(
        "<p>We received a request to reset your password.</p>"
        f'<p><a href="{escape(reset_url, quote=True)}">'
        "Reset your password</a></p>"
        "<p>If you did not request this, you can ignore this email.</p>",
        subtype="html",
    )

    with smtplib.SMTP(
        settings["SMTP_HOST"],
        int(settings["SMTP_PORT"]),
        timeout=10,
    ) as server:
        server.ehlo()
        server.starttls(context=ssl.create_default_context())
        server.ehlo()
        server.login(settings["SMTP_USERNAME"], settings["SMTP_PASSWORD"])
        server.send_message(message)