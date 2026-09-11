import random
import time
from datetime import datetime, timezone
from supabase import create_client

# Fill these locally or use environment variables.
SUPABASE_URL = "https://wvfvnwklkbpczcqtlyfy.supabase.co"
SUPABASE_SECRET_KEY = "PASTE_BACKEND_SECRET_KEY_HERE"

supabase = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)

BUSES = [
    {"id": "BUS_04", "route": "Gandhinagar → Ahmedabad", "route_code": "GNR-AHM-01"},
    {"id": "BUS_07", "route": "Ahmedabad → Gandhinagar", "route_code": "AHM-GNR-02"},
    {"id": "BUS_12", "route": "Chandkheda → Ahmedabad", "route_code": "CHK-AHM-03"},
]

EVENT_TYPES = [
    "pothole", "damaged_road", "missing_divider",
    "missing_zebra_crossing", "damaged_signboard",
    "waterlogging", "vehicle_density", "traffic_bottleneck",
    "pedestrian_risk", "incident_rash_driving", "incident_hit_and_run"
]

def make_event():
    bus = random.choice(BUSES)
    lat = random.uniform(23.05, 23.20)
    lon = random.uniform(72.57, 72.64)
    event_type = random.choice(EVENT_TYPES)

    metadata = {
        "source": "fleet_simulator",
        "simulation": True,
        "route": bus["route"],
        "route_code": bus["route_code"],
    }

    if event_type == "vehicle_density":
        metadata.update({
            "vehicle_count": random.randint(5, 40),
            "traffic_density": random.choice(["LOW", "MEDIUM", "HIGH"])
        })

    return {
        "event_type": event_type,
        "bus_id": bus["id"],
        "occurred_at": datetime.now(timezone.utc).isoformat(),
        "confidence": round(random.uniform(0.78, 0.98), 2),
        "geom": f"POINT({lon} {lat})",
        "metadata": metadata,
    }

if __name__ == "__main__":
    for _ in range(10):
        event = make_event()
        supabase.table("events").insert(event).execute()
        print("Inserted:", event["event_type"], event["bus_id"])
        time.sleep(1)
