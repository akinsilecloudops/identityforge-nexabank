
from datetime import datetime
from app import config
from app.timeutil import to_local


def detect_event(event, baseline):
    alerts = []
    agent_id = event["agent_id"]
    agent = baseline.get(agent_id)

    if not agent:
        return [{
            "type": "unknown_agent",
            "severity": "high",
            "agent_id": agent_id,
            "reason": "No baseline exists for this agent.",
        }]

    assigned_region = event["assigned_region"]
    region = event["region"]

    if region != assigned_region:
        alerts.append({
            "type": "region",
            "severity": "high",
            "agent_id": agent_id,
            "assigned_region": assigned_region,
            "seen_region": region,
            "device_id": event["device_id"],
            "reason": "Transaction region differs from assigned region.",
        })

    known_devices = agent.get("devices", {})
    if event["device_id"] not in known_devices:
        alerts.append({
            "type": "device",
            "severity": "high",
            "agent_id": agent_id,
            "device_id": event["device_id"],
            "reason": "Device has not appeared in the agent baseline.",
        })

    mean = agent.get("amount_mean", 0)
    stddev = agent.get("amount_stddev", 0)
    amount = float(event["amount"])

    if stddev > 0 and amount > mean + config.Z_LIMIT * stddev:
        alerts.append({
            "type": "amount",
            "severity": "high",
            "agent_id": agent_id,
            "amount": amount,
            "baseline_mean": mean,
            "reason": "Transaction amount is unusually high.",
        })

    timestamp = datetime.fromisoformat(
        event["event_time"].replace("Z", "+00:00")
    )
    hour = str(to_local(timestamp).hour)
    hour_share = agent.get("hour_share", {}).get(hour, 0)

    if hour_share < config.RARE_HOUR_SHARE:
        alerts.append({
            "type": "time",
            "severity": "medium",
            "agent_id": agent_id,
            "local_time": to_local(timestamp).strftime("%H:%M"),
            "past_activity_in_this_hour_percent": round(
                hour_share * 100, 2
            ),
            "device_id": event["device_id"],
            "reason": "Transaction occurred during a rare activity hour.",
        })

    return alerts
