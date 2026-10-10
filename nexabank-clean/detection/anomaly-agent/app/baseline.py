
import json
from collections import Counter, defaultdict
from pathlib import Path

from app import config


def train_baseline(jsonl_path):
    counts = Counter()
    amounts = defaultdict(list)
    regions = defaultdict(Counter)
    devices = defaultdict(Counter)
    hours = defaultdict(Counter)

    with open(jsonl_path, "r", encoding="utf-8-sig") as file:
        for line in file:
            if not line.strip():
                continue

            event = json.loads(line)
            agent = event["agent_id"]
            counts[agent] += 1
            amounts[agent].append(float(event["amount"]))
            regions[agent][event["region"]] += 1
            devices[agent][event["device_id"]] += 1

            from datetime import datetime
            from app.timeutil import to_local

            timestamp = datetime.fromisoformat(
                event["event_time"].replace("Z", "+00:00")
            )
            local_hour = to_local(timestamp).hour
            hours[agent][str(local_hour)] += 1

    baseline = {}

    for agent, count in counts.items():
        values = amounts[agent]
        mean = sum(values) / len(values)
        variance = sum((value - mean) ** 2 for value in values) / len(values)
        stddev = variance ** 0.5
        total_hours = sum(hours[agent].values())

        baseline[agent] = {
            "event_count": count,
            "amount_mean": mean,
            "amount_stddev": stddev,
            "regions": dict(regions[agent]),
            "devices": dict(devices[agent]),
            "hour_share": {
                hour: hour_count / total_hours
                for hour, hour_count in hours[agent].items()
            },
        }

    output = Path(config.BASELINE_PATH)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(baseline, indent=2),
        encoding="utf-8",
    )

    return baseline
