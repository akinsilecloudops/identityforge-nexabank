# NexaBank Anomaly Agent — Handover Guide

## 1. Project overview

This service validates transaction events, detects unusual activity using an agent baseline, stores events and alerts in SQLite, generates explanatory narratives, and can send alerts to Slack.

## 2. Requirements

- Python 3.12 (the current development environment uses Python 3.12.5)
- Git
- Optional for AI narratives: Ollama with `llama3.2:3b`
- Optional for Slack notifications: a configured Slack incoming webhook
- Optional for error monitoring: a configured Sentry DSN

## 3. Set up the environment

From the `detection/anomaly-agent/` directory, create and activate a virtual environment:

**Windows PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create your local `.env` file from `.env.example`. Configure your own secrets; never commit `.env`.

## 4. Generate and train a baseline

```powershell
python -m tools.generator normal
python -m tools.train_baseline --jsonl data/normal.jsonl
python -m tools.verify_state
```

The baseline is trained on synthetic normal transaction events. Do not treat synthetic results as proof of real-world fraud detection accuracy.

## 5. Run tests

```powershell
pytest -q
```

The initial handover target is 13 passing tests.

## 6. Run the API locally

Configure a strong `INGEST_API_KEY` in `.env`, then run:

```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Check health at `http://127.0.0.1:8000/health`.

The event ingestion endpoint is `POST /events` and requires the `X-API-Key` header. The API also provides `GET /stats`.

## 7. Configuration

See `.env.example` for supported environment variables, including the database/baseline directory, ingestion API key, Slack webhook, Ollama URL/model, detection thresholds, and Sentry DSN.

Keep real credentials in the approved password vault. Do not place secrets in source code, documentation, Git commits, or chat.

## 8. Current handover status

- Detector tests: passed during development.
- API tests: 13 passed during development.
- Baseline and database verification: passed during development.
- Slack delivery and live Ollama generation: must be verified before claiming those integrations work.
- Clean-clone verification and Git secret scanning: pending.
- AWS deployment and Wazuh integration: owned by Person 2.

## 9. Person 2 acceptance checklist

- [ ] Confirm access to the repository and required accounts.
- [ ] Clone the agreed handover commit/tag into a fresh directory.
- [ ] Create a new virtual environment and install dependencies.
- [ ] Configure a private `.env` with fresh credentials.
- [ ] Run `pytest -q` and `python -m tools.verify_state`.
- [ ] Verify the API's health and authentication behavior.
- [ ] Continue with the assigned setup and Steps 15–25.
