
import pytest


@pytest.fixture
def baseline():
    return {
        "AG-1001": {
            "event_count": 100,
            "amount_mean": 10000.0,
            "amount_stddev": 2000.0,
            "regions": {"Lagos": 100},
            "devices": {"TAB-1001": 100},
            "hour_share": {"10": 0.5, "2": 0.0},
        }
    }


@pytest.fixture
def normal_event():
    return {
        "event_time": "2026-10-10T09:00:00Z",
        "event_type": "transaction",
        "agent_id": "AG-1001",
        "assigned_region": "Lagos",
        "region": "Lagos",
        "device_id": "TAB-1001",
        "cert_dn": "CN=AG-1001,OU=Agents,O=NexaBank",
        "amount": 10000.0,
        "result": "success",
    }
