#!/usr/bin/env python3
import json
import csv
from urllib.request import urlopen
import time

# ==============================
# Налаштування
# ==============================
YEAR = 2026
OUTPUT_CSV = "f1_sessions_2026.csv"
BASE_API = "https://api.openf1.org/v1"
SLEEP_BETWEEN = 1

# ==============================
# API
# ==============================
def get_json(url):
    try:
        with urlopen(url, timeout=10) as r:
            data = json.loads(r.read().decode("utf-8"))
            time.sleep(SLEEP_BETWEEN)
            return data
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

# ==============================
# Отримати всі сесії року
# ==============================
def get_sessions(year):
    url = f"{BASE_API}/sessions?year={year}"
    return get_json(url)

# ==============================
# Запис у CSV
# ==============================
def save_sessions_to_csv(sessions, filename):
    fieldnames = [
        "session_key",
        "meeting_key",
        "session_type",
        "session_name",
        "date_start",
        "date_end",
        "circuit_short_name",
        "country_name",
        "location",
        "year"
    ]

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for s in sessions:
            writer.writerow({
                "session_key": s.get("session_key"),
                "meeting_key": s.get("meeting_key"),
                "session_type": s.get("session_type"),
                "session_name": s.get("session_name"),
                "date_start": s.get("date_start"),
                "date_end": s.get("date_end"),
                "circuit_short_name": s.get("circuit_short_name"),
                "country_name": s.get("country_name"),
                "location": s.get("location"),
                "year": s.get("year"),
            })

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    sessions = get_sessions(YEAR)

    print(f"Fetched {len(sessions)} sessions for {YEAR}")

    # опційно: тільки Race
    # sessions = [s for s in sessions if s["session_type"] == "Race"]

    save_sessions_to_csv(sessions, OUTPUT_CSV)

    print(f"Saved to {OUTPUT_CSV}")
