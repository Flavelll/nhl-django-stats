-- ==========================================
-- ТАБЛИЦІ
-- ==========================================

DROP TABLE IF EXISTS bx;
DROP TABLE IF EXISTS story;

CREATE TABLE bx (
    GameDate INTEGER,
    GameId INTEGER,
    Season INTEGER,
    GameType INTEGER,
    Sweater_number INTEGER,
    Name TEXT,
    Position TEXT,
    Team TEXT,
    Opponent TEXT,
    Playerid INTEGER,
    Goals INTEGER,
    Assists INTEGER,
    Points INTEGER,
    PlusMinus INTEGER,
    PIM INTEGER,
    Hits INTEGER,
    PowerPlayGoals INTEGER,
    SOG INTEGER,
    FaceoffWinning REAL,
    TOI TEXT,
    Blockedshots INTEGER,
    Shifts INTEGER,
    Giveaways INTEGER,
    Takeaways INTEGER,
    EvenStrengthShotsAgainst INTEGER,
    PowerPlayShotsAgainst INTEGER,
    ShorthandedShotsAgainst INTEGER,
    SaveShotsAgainst INTEGER,
    save_pct REAL,
    EvenStrengthGoalsAgainst INTEGER,
    PowerPlayGoalsAgainst INTEGER,
    ShorthandedGoalsAgainst INTEGER,
    GoalsAgainst INTEGER,
    starter BOOLEAN,
    ShotsAgainst INTEGER,
    Saves INTEGER
);

CREATE TABLE story (
    gameId INTEGER PRIMARY KEY,
    gameDate TEXT,
    homeTeam TEXT,
    awayTeam TEXT,
    homeFOW REAL,
    awayFOW REAL,
    homePPF INTEGER,
    awayPPF INTEGER
);

-- ==========================================
-- ЗВИЧАЙНІ VIEW замість MATERIALIZED VIEW
-- ==========================================

DROP VIEW IF EXISTS mv_team;
CREATE VIEW mv_team AS
SELECT team, season, gametype,
    COUNT(DISTINCT GameId) AS games,
    SUM(Goals) AS GF,
    SUM(PowerPlayGoals) AS ppg,
    SUM(SOG) AS sog,
    SUM(PIM) AS pim,
    SUM(Blockedshots) AS blc,
    SUM(Giveaways) AS give,
    SUM(Takeaways) AS take,
    SUM(Hits) AS hits,
    SUM(GoalsAgainst) as GA,
    SUM(ShotsAgainst) as SA,
    ROUND(SUM(SOG) * 1.0 / COUNT(DISTINCT GameId), 2) AS avgsog,
    ROUND(SUM(SOG) * 1.0 / SUM(Shifts), 3) AS sps,
    ROUND(SUM(FaceoffWinning) * 1.0 / COUNT(DISTINCT GameId), 3) AS FOW,
    ROUND(SUM(save_pct) * 1.0 / COUNT(DISTINCT GameId), 3) AS SAVE
FROM bx
GROUP BY team, season, gametype;

DROP VIEW IF EXISTS mv_players;
CREATE VIEW mv_players AS
SELECT
    Name AS name,
    Team AS team,
    Position AS position,
    Season AS season,
    GameType AS gametype,
    SUM(Goals) AS goals,
    SUM(PowerPlayGoals) AS ppg,
    SUM(SOG) AS sog,
    ROUND(SUM(SOG) * 1.0 / NULLIF(SUM(Shifts),0), 2) AS sps,
    SUM(Assists) AS ast,
    SUM(Points) AS pts,
    SUM(PlusMinus) AS plmn,
    SUM(Shifts) AS shft,
    SUM(PIM) AS pim,
    SUM(Blockedshots) AS blc,
    SUM(Giveaways) AS give,
    SUM(Takeaways) AS take,
    SUM(Hits) AS hits
FROM bx
GROUP BY Team, Name, Position, Season, GameType;

DROP VIEW IF EXISTS mv_team_game;
CREATE VIEW mv_team_game AS
SELECT
    Team AS team,
    GameId AS gameid,
    Opponent AS opponent,
    Season AS season,
    GameType AS gametype,
    SUM(Goals) AS goals,
    SUM(SOG) AS sog,
    SUM(PowerPlayGoals) AS ppg,
    SUM(Shifts) AS shifts,
    SUM(PIM) AS pim,
    SUM(Blockedshots) AS blocked,
    SUM(Giveaways) AS giveaways,
    SUM(Takeaways) AS takeaways,
    SUM(Hits) AS hits,
    SUM(GoalsAgainst) AS ga,
    SUM(ShotsAgainst) AS sa,
    ROUND(SUM(SOG) * 1.0 / NULLIF(SUM(Shifts),0), 3) AS sps
FROM bx
GROUP BY Team, Opponent, GameId, Season, GameType;

CREATE UNIQUE INDEX IF NOT EXISTS idx_bx_unique
ON bx (GameId, Playerid);

CREATE TABLE f1_sessions (
    session_key INT PRIMARY KEY,
    meeting_key INT NOT NULL,

    session_type VARCHAR(20) NOT NULL,
    session_name VARCHAR(50),

    date_start TIMESTAMPTZ NOT NULL,
    date_end TIMESTAMPTZ,

    circuit_short_name VARCHAR(100),
    country_name VARCHAR(100),
    location VARCHAR(100),

    year INT NOT NULL
);

CREATE TABLE f1_laps (
    meeting_key INT,
    session_key INT,
    driver_number INT,
    lap_number INT,
    date_start TIMESTAMP,
    lap_duration FLOAT,
    sector1 FLOAT,
    sector2 FLOAT,
    sector3 FLOAT,
    is_pit_out BOOLEAN
);
