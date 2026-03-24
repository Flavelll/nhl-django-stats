import requests
from pymongo import MongoClient

# ----------------------------------
# GLOBAL CONFIG
# ----------------------------------

SEASON = 2025
START_GAME = 1
END_GAME = 1398

CURRENT_COUNT = 0

MONGO_DB = "nhl_db"
MONGO_COLLECTION = "bx"


# ----------------------------------
# Mongo connection
# ----------------------------------
# створюємо один конект на весь скрипт
# щоб не відкривати новий для кожної гри

client = MongoClient("mongodb://localhost:27017")

db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]


# ----------------------------------
# ФУНКЦІЯ: fetch + insert
# ----------------------------------
def insert_game(game_id):
    """
    Логіка повністю повторює bash функцію:
    1. робимо HTTP запит
    2. перевіряємо що JSON валідний
    3. перевіряємо що існує playerByGameStats
    4. upsert у Mongo
    """

    global CURRENT_COUNT

    url = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/boxscore"

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()  # HTTP error -> exception
    except Exception as e:
        print(f"\n[HTTP ERROR] {game_id} -> {e}")
        return

    try:
        data = r.json()  # JSON -> python dict
    except Exception:
        print(f"\n[ERROR] Invalid JSON for {game_id}")
        return

    # аналог jq '.playerByGameStats'
    if "playerByGameStats" not in data:
        return

    # Mongo upsert
    collection.update_one(
        {"id": data["id"]},  # фільтр
        {"$set": data},      # що записуємо
        upsert=True          # якщо нема -> insert
    )

    CURRENT_COUNT += 1

    print(f"\r[{CURRENT_COUNT}] Fetching {game_id}...", end="")


# ----------------------------------
# REGULAR SEASON
# ----------------------------------
def regular_season():

    for game in range(START_GAME, END_GAME + 1):

        # аналог seq -f %04g
        game_str = f"{game:04d}"

        game_id = f"{SEASON}02{game_str}"

        insert_game(game_id)


# ----------------------------------
# PLAYOFFS
# ----------------------------------
def playoffs():

    # три вкладених цикли повністю повторюють bash логіку
    # ROUND -> SERIES -> GAME

    for round_ in range(1, 5):

        for series in range(1, 9):

            for game in range(1, 8):

                game_id = f"{SEASON}030{round_}{series}{game}"

                insert_game(game_id)


# ----------------------------------
# MAIN
# ----------------------------------

if __name__ == "__main__":

    regular_season()
    playoffs()

    print("\nDone")
