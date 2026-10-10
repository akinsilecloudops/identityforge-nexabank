
import argparse

from app.baseline import train_baseline


def main():
    parser = argparse.ArgumentParser(
        description="Train a baseline from normal transaction events."
    )
    parser.add_argument(
        "--jsonl",
        default="data/normal.jsonl",
        help="Path to the normal transaction JSONL file.",
    )
    args = parser.parse_args()

    baseline = train_baseline(args.jsonl)
    print(f"Baseline saved for {len(baseline)} agents.")
    for agent, details in baseline.items():
        print(f"{agent}: {details['event_count']} events")


if __name__ == "__main__":
    main()
