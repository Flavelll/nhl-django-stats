# queries.py

from django.db import connection



# ==========================================================
# 🔹 BASE SQL
# ==========================================================


def fetch_all(query: str, params=None):
    with connection.cursor() as cursor:
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]




# ==========================================================
# 🔹 TEAM STATS OVERALL
# ==========================================================
def get_team_total(teams, seasons, game_types):
    # конвертуємо списки у рядки для SQLite
    teams = teams or []
    seasons = seasons or []
    game_types = game_types or []

    if not teams or not seasons or not game_types:
        # якщо хочеш, можна відразу повернути порожній список
        return []

    teams_str = ','.join(f"'{t}'" for t in teams)
    seasons_str = ','.join(str(s) for s in seasons)
    gametypes_str = ','.join(str(g) for g in game_types)

    sql = f"""
        SELECT *
        FROM mv_team
        WHERE team IN ({teams_str})
          AND season IN ({seasons_str})
          AND gametype IN ({gametypes_str})
    """
    return fetch_all(sql)


# ==========================================================
# 🔹 TEAM STATS LAST N OVERALL
# ==========================================================

def get_team_games(teams, seasons, game_types):
    teams = teams or []
    seasons = seasons or []
    game_types = game_types or []

    if not teams or not seasons or not game_types:
        # якщо хочеш, можна відразу повернути порожній список
        return []

    teams_str = ','.join(f"'{t}'" for t in teams)
    seasons_str = ','.join(str(s) for s in seasons)
    gametypes_str = ','.join(str(g) for g in game_types)

    sql = f"""
        SELECT *
        FROM mv_team_game
        WHERE team IN ({teams_str})
          AND season IN ({seasons_str})
          AND gametype IN ({gametypes_str})
        ORDER BY gameid DESC
    """
    return fetch_all(sql)



# ==========================================================
# 🔹 PLAYER STATS OVERALL
# ==========================================================

def get_players_total(teams, seasons, game_types):
    teams = teams or []
    seasons = seasons or []
    game_types = game_types or []

    if not teams or not seasons or not game_types:
        # якщо хочеш, можна відразу повернути порожній список
        return []

    teams_str = ','.join(f"'{t}'" for t in teams)
    seasons_str = ','.join(str(s) for s in seasons)
    gametypes_str = ','.join(str(g) for g in game_types)

    sql = f"""
        SELECT *
        FROM mv_players
        WHERE team IN ({teams_str})
          AND season IN ({seasons_str})
          AND gametype IN ({gametypes_str})
          AND position != 'G'
        ORDER BY pts DESC
    """
    return fetch_all(sql)


# Goalies

def get_goalies_total(teams, seasons, game_types):
    teams = teams or []
    seasons = seasons or []
    game_types = game_types or []

    if not teams or not seasons or not game_types:
        # якщо хочеш, можна відразу повернути порожній список
        return []

    teams_str = ','.join(f"'{t}'" for t in teams)
    seasons_str = ','.join(str(s) for s in seasons)
    gametypes_str = ','.join(str(g) for g in game_types)

    sql = f"""
        SELECT *
        FROM mv_players
        WHERE team IN ({teams_str})
          AND season IN ({seasons_str})
          AND gametype IN ({gametypes_str})
          AND position = 'G'
        ORDER BY pts DESC
    """
    return fetch_all(sql)

#







# ==========================================================
#   ALL TEAMS AGGREGATED STAT
# ==========================================================

def get_agg():

    sql = """
        SELECT
          t1.team,
          t1."SF", t2."SA",
          t1."GF", t2."GA",
          t1."PPGF", t2."PPGA",
          t1."avgSF", t2."avgSA",
          t2."PPSF",t1."PPSA",
          ROUND (t1."SAVE%", 3),
          (COALESCE(t3."PPFhome", 0) + COALESCE(t4."PPFaway", 0)) AS "PPF",
          (COALESCE(t3."PPAhome", 0) + COALESCE(t4."PPAaway", 0)) AS "PPA",


          CASE
            WHEN (COALESCE(t3."PPFhome", 0) + COALESCE(t4."PPFaway", 0)) > 0
            THEN ROUND(
              (COALESCE(t1."PPGF", 0) * 100.0) /
              (COALESCE(t3."PPFhome", 0) + COALESCE(t4."PPFaway", 0)), 2
            )
            ELSE 0
          END AS "PPG%",

          CASE
            WHEN (COALESCE(t3."PPAhome", 0) + COALESCE(t4."PPAaway", 0)) > 0
            THEN 100 - ROUND(
              (COALESCE(t2."PPGA", 0) * 100.0) /
              (COALESCE(t3."PPAhome", 0) + COALESCE(t4."PPAaway", 0)), 2
            )
            ELSE 0
          END AS "Kill%",
          CASE
            WHEN (COALESCE(t3."FWFhome", 0) + COALESCE(t4."FWFaway", 0)) > 0
            THEN ROUND(
              (COALESCE(t3."FWFhome", 0) + COALESCE(t4."FWFaway", 0)) * 100.0 /
              ((COALESCE(t3."FWFhome", 0) + COALESCE(t4."FWFaway", 0)) +
              (COALESCE(t3."FWAhome", 0) + COALESCE(t4."FWAaway", 0))), 2
            )
            ELSE 0
          END AS "FOW%"

        FROM
          (
            SELECT
              team,
              SUM(goals) AS "GF",
              SUM(sog) AS "SF",
              SUM(powerplaygoals) AS "PPGF",
              SUM(powerplayshotsagainst) AS "PPSA",
              ROUND(SUM (save_pct) * 1.00 / COUNT(DISTINCT gameid), 3) AS "SAVE%",
              ROUND (SUM(sog) * 1.00 / COUNT(DISTINCT gameid), 3) AS "avgSF"

            FROM bx
            GROUP BY team
          ) t1
        LEFT JOIN
          (
            SELECT
              opponent,
              SUM(goals) AS "GA",
              SUM(sog) AS "SA",
              SUM(powerplaygoals) AS "PPGA",
              SUM(powerplayshotsagainst) AS "PPSF",
              ROUND (SUM(sog) * 1.00 / COUNT(DISTINCT gameid), 3) AS "avgSA"

            FROM bx
            GROUP BY opponent
          ) t2
        ON t1.team = t2.opponent
        LEFT JOIN
          (
            SELECT
              hometeam,
              SUM(homePPF) AS "PPFhome",
              SUM(awayPPF) AS "PPAhome",
              SUM(homeFOW) AS "FWFhome",
              SUM(awayFOW) AS "FWAhome"
            FROM story
            GROUP BY hometeam
          ) t3
        ON t1.team = t3.hometeam
        LEFT JOIN
          (
            SELECT
              awayteam,
              SUM(awayPPF) AS "PPFaway",
              SUM(homePPF) AS "PPAaway",
              SUM(awayFOW) AS "FWFaway",
              SUM(homeFOW) AS "FWAaway"
            FROM story
            GROUP BY awayteam
          ) t4
        ON t1.team = t4.awayteam;
    """
    return fetch_all(sql)





# ==========================================================
# 🔹 Compare matrix
# ==========================================================
def get_compare_teams(teams, opponents, seasons, gametypes):

    sql = """
        SELECT
            team, position,
            gamedate, season, gametype,
            SUM(goals) AS GF,
            SUM(powerplaygoals) AS ppg,
            SUM(sog) AS sog,
            SUM(assists) AS ast,
            SUM(pim) AS pim,
            SUM(blockedshots) AS blc,
            SUM(giveaways) AS give,
            SUM(takeaways) AS take,
            SUM(hits) AS hits,
            SUM(goalsagainst) as GA,
            SUM(shotsagainst) as SA,
            SUM(powerplayshotsagainst) as PPGA,
            SUM(shorthandedgoalsagainst)  as SHGA,
            SUM(saveshotsagainst) as SVSA,
            SUM(evenstrengthshotsagainst) as ESA,
            SUM(evenstrengthgoalsagainst) as EGA,
            ROUND(SUM(faceoffwinning) / count(distinct gameid), 3) as FOW,
            ROUND(SUM(save_pct) / COUNT(DISTINCT gameid), 3) AS SAVE
        FROM mv_team
        group by gamedate, team, season, gametype, position;
    """

    params = [
        teams, seasons, gametypes,
        opponents, seasons, gametypes
    ]

    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        return cursor.fetchall()
# ==========================================================
# 🔹 TEAM STATS LAST N TOTAL
# ==========================================================


# ==========================================================
# 🔹 PLAYER STATS LAST N GAMES
# ==========================================================

# ==========================================================

# 🔹 TIMELINE TEAM STATS LAST N GAMES
# ==========================================================


# ==========================================================
# 🔹 TIMELINE PLAYER STATS LAST N GAMES
# ==========================================================

# ==========================================================
# 🔹 Filter Func
# ==========================================================
def build_filters(
    seasons=None,
    game_types=None,
    games=None,
    game_date_from=None,
    game_date_to=None,
    teams=None,
    opponents=None,
    players=None,
    conference=None,
    position=None,
    table_alias=None,
):
    conditions = []
    params = []

    prefix = f"{table_alias}." if table_alias else ""

    # LIST FILTERS
    if seasons:
        conditions.append(f"{prefix}season = ANY(%s)")
        params.append(seasons)
    if game_types:
        conditions.append(f"{prefix}gametype = ANY(%s)")
        params.append(game_types)
    if games:
        conditions.append(f"{prefix}gameid = ANY(%s)")
        params.append(games)
    if teams:
        conditions.append(f"{prefix}team = ANY(%s)")
        params.append(teams)
    if opponents:
        conditions.append(f"{prefix}opponent = ANY(%s)")
        params.append(opponents)
    if players:
        conditions.append(f"{prefix}player = ANY(%s)")
        params.append(players)

    # SCALAR FILTERS
    if position:
        conditions.append(f"{prefix}position = %s")
        params.append(position)
    if conference:
        conditions.append(f"{prefix}conference = %s")
        params.append(conference)

    # DATE RANGE
    if game_date_from:
        conditions.append(f"{prefix}gamedate >= %s")
        params.append(game_date_from)
    if game_date_to:
        conditions.append(f"{prefix}gamedate <= %s")
        params.append(game_date_to)

    return conditions, params


