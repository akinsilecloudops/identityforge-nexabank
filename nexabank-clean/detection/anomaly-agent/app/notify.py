
import requests

from app import config


def send_alert(alert):
    """Send an alert to Slack if a webhook URL is configured."""

    webhook_url = config.SLACK_WEBHOOK_URL

    if not webhook_url:
        return {
            "sent": False,
            "reason": "Slack webhook is not configured.",
        }

    message = (
        f"*NexaBank Anomaly Alert*\n"
        f"*Type:* {alert.get('type', 'unknown')}\n"
        f"*Severity:* {alert.get('severity', 'medium')}\n"
        f"*Agent:* {alert.get('agent_id', 'unknown')}\n"
        f"*Reason:* {alert.get('reason', 'No reason provided.')}"
    )

    try:
        response = requests.post(
            webhook_url,
            json={"text": message},
            timeout=10,
        )
        response.raise_for_status()

        return {"sent": True}

    except requests.RequestException as exc:
        return {
            "sent": False,
            "reason": str(exc),
        }
