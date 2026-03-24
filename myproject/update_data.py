#!/usr/bin/env python3
import requests
import sqlite3
import time

# ==============================
# Налаштування
# ==============================
SEASON = 2025
DB_PATH = "/app/db.sqlite3"
SLEEP_BETWEEN = 0.05

# ==============================
# Допоміжні функції
# ==============================
def fetch_game(game_id):
    url = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/boxscore"
    try:
        r = requests.get(url, timeout=10)
        return r.json()
    except:
        return None

def safe_get(d, key, default=0):
    val = d.get(key)
    return val if val is not None else default

def extract_rows(data):
    rows = []

    gameid = data.get("id")
    gamedate = data.get("gameDate")
    season = data.get("season")
    gametype = data.get("gameType")

    home = data.get("homeTeam", {}).get("abbrev")
    away = data.get("awayTeam", {}).get("abbrev")

    stats = data.get("playerByGameStats", {})
    if not stats:
        return rows

    def process(team_key, team, opponent):
        for group in ["forwards", "defense", "goalies"]:
            for p in stats.get(team_key, {}).get(group, []):
                row = (
                    gamedate,
                    gameid,
                    season,
                    gametype,
                    safe_get(p, "sweaterNumber"),
                    p.get("name", {}).get("default"),
                    p.get("position"),
                    team,
                    opponent,
                    safe_get(p, "playerId"),
                    safe_get(p, "goals"),
                    safe_get(p, "assists"),
                    safe_get(p, "points"),
                    safe_get(p, "plusMinus"),
                    safe_get(p, "pim"),
                    safe_get(p, "hits"),
                    safe_get(p, "powerPlayGoals"),
                    safe_get(p, "sog"),
                    safe_get(p, "faceoffWinningPctg"),
                    p.get("toi"),
                    safe_get(p, "blockedShots"),
                    safe_get(p, "shifts"),
                    safe_get(p, "giveaways"),
                    safe_get(p, "takeaways"),
                    safe_get(p, "evenStrengthShotsAgainst"),
                    safe_get(p, "powerPlayShotsAgainst"),
                    safe_get(p, "shorthandedShotsAgainst"),
                    safe_get(p, "saveShotsAgainst"),
                    safe_get(p, "savePctg"),
                    safe_get(p, "evenStrengthGoalsAgainst"),
                    safe_get(p, "powerPlayGoalsAgainst"),
                    safe_get(p, "shorthandedGoalsAgainst"),
                    safe_get(p, "goalsAgainst"),
                    1 if p.get("starter") else 0,
                    safe_get(p, "shotsAgainst"),
                    safe_get(p, "saves")
                )
                rows.append(row)

    process("homeTeam", home, away)
    process("awayTeam", away, home)

    return rows

def insert_rows(cursor, rows):
    cursor.executemany("""
        INSERT OR IGNORE INTO bx (
            GameDate, GameId, Season, GameType,
            Sweater_number, Name, Position, Team, Opponent, Playerid,
            Goals, Assists, Points, PlusMinus, PIM, Hits,
            PowerPlayGoals, SOG, FaceoffWinning, TOI,
            Blockedshots, Shifts, Giveaways, Takeaways,
            EvenStrengthShotsAgainst, PowerPlayShotsAgainst, ShorthandedShotsAgainst,
            SaveShotsAgainst, save_pct,
            EvenStrengthGoalsAgainst, PowerPlayGoalsAgainst, ShorthandedGoalsAgainst,
            GoalsAgainst, starter,
            ShotsAgainst, Saves
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, rows)


def get_last_game_id(cursor):
    cursor.execute("SELECT MAX(GameId) FROM bx")
    result = cursor.fetchone()[0]
    return result

# ==============================
# Головна функція
# ==============================
def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # --- отримуємо останній GameId ---
    last_game_id = get_last_game_id(cursor)
    print("Останній GameId у базі:", last_game_id)

    start_reg = 1
    start_po = None

    if last_game_id:
        last_game_id = str(last_game_id)

        # ---------------- REGULAR ----------------
        if last_game_id.startswith(f"{SEASON}02"):
            start_reg = int(last_game_id[-4:]) + 1
            print(f"Продовжуємо регулярку з гри: {start_reg}")

        # ---------------- PLAYOFF ----------------
        elif last_game_id.startswith(f"{SEASON}03"):
            # формат: 2025 03 R S G
            round_ = int(last_game_id[6])
            series = int(last_game_id[7])
            game = int(last_game_id[8])

            start_po = (round_, series, game + 1)
            print(f"Продовжуємо плей-оф з: round={round_}, series={series}, game={game+1}")

    # ---------------- REGULAR SEASON ----------------
    if start_po is None:  # якщо ще не було плей-оф
        for game in range(start_reg, 1400):
            game_id = f"{SEASON}02{game:04d}"
            print("REG:", game_id)

            data = fetch_game(game_id)
            if not data:
                print(f"Немає даних для {game_id}")
                continue

            rows = extract_rows(data)
            if rows:
                insert_rows(cursor, rows)
                conn.commit()
                print(f"Вставлено {len(rows)} рядків для {game_id}")

            time.sleep(SLEEP_BETWEEN)

    # ---------------- PLAYOFFS ----------------
    start_round = 1
    start_series = 1
    start_game = 1

    if start_po:
        start_round, start_series, start_game = start_po

    for round_ in range(start_round, 5):
        max_series = {1: 8, 2: 4, 3: 2, 4: 1}[round_]

        for series in range(start_series if round_ == start_round else 1, max_series + 1):

            for game in range(start_game if (round_ == start_round and series == start_series) else 1, 8):

                game_id = f"{SEASON}030{round_}{series}{game}"
                print("PO:", game_id)

                data = fetch_game(game_id)
                if not data:
                    print(f"Немає даних для {game_id}")
                    continue

                rows = extract_rows(data)
                if rows:
                    insert_rows(cursor, rows)
                    conn.commit()
                    print(f"Вставлено {len(rows)} рядків для {game_id}")

                time.sleep(SLEEP_BETWEEN)

        start_series = 1
        start_game = 1

    conn.close()
    print("Готово! Всі нові ігри додані.")
# ==============================
# Старт
# ==============================
if __name__ == "__main__":
    main()
