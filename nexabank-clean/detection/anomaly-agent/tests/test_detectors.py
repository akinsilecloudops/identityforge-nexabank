
from app.detectors import detect_event


def test_normal_event_has_no_alerts(normal_event, baseline):
    assert detect_event(normal_event, baseline) == []


def test_region_mismatch_is_detected(normal_event, baseline):
    normal_event["region"] = "Kano"
    alerts = detect_event(normal_event, baseline)
    assert any(alert["type"] == "region" for alert in alerts)


def test_unknown_device_is_detected(normal_event, baseline):
    normal_event["device_id"] = "UNKNOWN-123"
    alerts = detect_event(normal_event, baseline)
    assert any(alert["type"] == "device" for alert in alerts)


def test_unusually_large_amount_is_detected(normal_event, baseline):
    normal_event["amount"] = 50000.0
    alerts = detect_event(normal_event, baseline)
    assert any(alert["type"] == "amount" for alert in alerts)


def test_unknown_agent_is_detected(normal_event, baseline):
    normal_event["agent_id"] = "AG-9999"
    alerts = detect_event(normal_event, baseline)
    assert alerts[0]["type"] == "unknown_agent"


def test_rare_hour_is_detected(normal_event, baseline):
    normal_event["event_time"] = "2026-10-10T01:00:00Z"
    alerts = detect_event(normal_event, baseline)
    assert any(alert["type"] == "time" for alert in alerts)
