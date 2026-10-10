
import requests

from app import config


def generate_narrative(alert):
    """Turn a detection alert into a clear explanation and action."""

    risk_level = alert.get("severity", "medium").lower()

    fallback = {
        "summary": (
            f"An anomaly of type '{alert.get('type', 'unknown')}' "
            f"was detected for agent {alert.get('agent_id', 'unknown')}."
        ),
        "risk_level": risk_level
        if risk_level in {"low", "medium", "high"}
        else "medium",
        "recommended_action": (
            "Review the transaction details and verify the agent, "
            "device, and transaction context before taking action."
        ),
    }

    prompt = f"""
You are a financial fraud monitoring assistant.
Analyze the following anomaly alert.

Alert:
{alert}

Return ONLY a valid JSON object with these three fields:
- summary: a concise explanation of the anomaly
- risk_level: low, medium, or high
- recommended_action: a practical next step

Do not claim fraud is confirmed. Explain uncertainty when appropriate.
"""

    try:
        response = requests.post(
            f"{config.OLLAMA_URL}/api/generate",
            json={
                "model": config.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json",
            },
            timeout=config.OLLAMA_TIMEOUT,
        )
        response.raise_for_status()

        import json

        result = json.loads(response.json()["response"])

        if (
            not isinstance(result, dict)
            or not all(
                key in result
                for key in (
                    "summary",
                    "risk_level",
                    "recommended_action",
                )
            )
            or result["risk_level"] not in {"low", "medium", "high"}
        ):
            return fallback

        return result

    except (requests.RequestException, ValueError, KeyError, TypeError):
        return fallback
