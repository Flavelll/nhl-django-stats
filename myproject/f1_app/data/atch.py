#!/usr/bin/env python3
import json
import csv
from urllib.request import urlopen
import time
import os

# ==============================
# Налаштування
# ==============================
YEAR = 2026
SESSION_TYPES = ["Race"]  # можна: ["Race", "Qualifying", "Practice"]
DRIVER_NUMBERS = [44, 63, 16]  # або None = всі драйвери
OUTPUT_CSV = "f1_laps_2026.csv"

BASE_API = "https://api.openf1.org/v1"
SLEEP_BETWEEN = 1
MAX_RETRIES = 5
BACKOFF = 5

# ==============================
# API helper
# ==============================
def get_json(url):
    for attempt in range(1, MAX_RETRIES+1):
        try:
            with urlopen(url, timeout=15) as r:
                data = json.loads(r.read().decode("utf-8"))
                time.sleep(SLEEP_BETWEEN)
                return data
        except Exception as e:
            if hasattr(e, 'code') and e.code == 429:
                wait = BACKOFF * attempt
                print(f"429 retry in {wait}s...")
                time.sleep(wait)
                continue
            print(f"Error: {url} -> {e}")
            time.sleep(SLEEP_BETWEEN)
            return []
    return []

# ==============================
# Отримати всі сесії року
# ==============================
def get_sessions(year):
    url = f"{BASE_API}/sessions?year={year}"
    return get_json(url)

# ==============================
# Отримати драйверів сесії
# ==============================
def get_drivers(session_key):
    url = f"{BASE_API}/drivers?session_key={session_key}"
    data = get_json(url)
    return [d["driver_number"] for d in data]

# ==============================
# Отримати лапи
# ==============================
def get_laps(session_key, driver_number):
    url = f"{BASE_API}/laps?session_key={session_key}&driver_number={driver_number}"
    return get_json(url)

# ==============================
# CSV writer
# ==============================
FIELDNAMES = [
    "meeting_key", "session_key", "driver_number", "lap_number", "date_start",
    "lap_duration", "duration_sector_1", "duration_sector_2", "duration_sector_3",
    "st_speed", "i1_speed", "i2_speed", "is_pit_out_lap"
]

def append_to_csv(rows, filename):
    write_header = not os.path.exists(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k) for k in FIELDNAMES})

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    sessions = get_sessions(YEAR)
    print(f"Found {len(sessions)} sessions")

    # фільтр по типу сесії
    sessions = [s for s in sessions if s["session_type"] in SESSION_TYPES]

    print(f"Filtered to {len(sessions)} sessions: {SESSION_TYPES}")

    for s in sessions:
        session_key = s["session_key"]
        print(f"\nSession {session_key}: {s['session_name']} ({s['location']})")

        # драйвери
        if DRIVER_NUMBERS:
            drivers = DRIVER_NUMBERS
        else:
            drivers = get_drivers(session_key)

        for driver in drivers:
            laps = get_laps(session_key, driver)

            # фільтр (опційно)
            laps = [l for l in laps if not l.get("is_pit_out_lap")]

            print(f"  Driver {driver}: {len(laps)} laps")

            if laps:
                append_to_csv(laps, OUTPUT_CSV)

    print(f"\nDone. Data saved to {OUTPUT_CSV}")
