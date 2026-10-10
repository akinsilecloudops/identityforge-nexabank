
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

AGENTS = {
    "AG-1001": "Lagos",
    "AG-1002": "Abuja",
    "AG-1003": "Port Harcourt",
}

OUTPUT_DIR = Path("data")


def generate_event(agent_id, assigned_region, when, attack=False):
    if attack:
        region = "Kano" if assigned_region != "Kano" else "Lagos"
        amount = random.uniform(500_000, 2_000_000)
        result = random.choice(["success", "failure"])
        device_id = f"UNKNOWN-{random.randint(100, 999)}"
    else:
        region = assigned_region
        amount = round(random.uniform(1_000, 50_000), 2)
        result = random.choices(
            ["success", "failure"], weights=[0.96, 0.04]
        )[0]
        device_id = f"TAB-{agent_id[-4:]}"

    return {
        "event_time": when.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "event_type": "transaction",
        "agent_id": agent_id,
        "assigned_region": assigned_region,
        "region": region,
        "device_id": device_id,
        "cert_dn": f"CN={agent_id},OU=Agents,O=NexaBank",
        "amount": round(amount, 2),
        "result": result,
    }


def main(mode="normal"):
    if mode not in {"normal", "attack"}:
        raise SystemExit("Mode must be 'normal' or 'attack'")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"{mode}.jsonl"
    now = datetime.now(timezone.utc).replace(microsecond=0)
    events = []

    if mode == "normal":
        for agent_id, region in AGENTS.items():
            for _ in range(500):
                offset_minutes = random.randint(0, 60 * 24 * 30)
                when = now - timedelta(minutes=offset_minutes)
                events.append(
                    generate_event(agent_id, region, when)
                )
        events.sort(key=lambda item: item["event_time"])
    else:
        for i in range(62):
            agent_id, assigned_region = list(AGENTS.items())[i % 3]
            when = now - timedelta(minutes=61 - i)
            events.append(
                generate_event(agent_id, assigned_region, when, attack=True)
            )

    with output_file.open("w", encoding="utf-8") as file:
        for event in events:
            file.write(json.dumps(event) + "\n")

    print(f"Generated {len(events)} {mode} events: {output_file}")


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else "normal")
