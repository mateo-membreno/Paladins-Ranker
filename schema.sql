PRAGMA foreign_keys = ON;

CREATE TABLE match{
    match_id INTEGER PRIMARY KEY NOT NULL,
    date DATE NOT NULL,
    match_length INTEGER NOT NULL,
    game_mode VARCHAR(30) NOT NULL,
    team_one_score INTEGER NOT NULL,
    team_two_score INTEGER NOT NULL,
    winning_team INTEGER NOT NULL,
    map VARCHAR(30) NOT NULL,
    ban_1 VARCHAR(30) NOT NULL,
    ban_2 VARCHAR(30) NOT NULL,
    ban_3 VARCHAR(30) NOT NULL,
    ban_4 VARCHAR(30) NOT NULL
}

CREATE TABLE player{
    match_id INTEGER NOT NULL,
    team_number INTEGER NOT NULL,
    champion VARCHAR(30) NOT NULL,
    username VARCHAR(30) NOT NULL,
    pick_number INTEGER NOT NULL,
    champ_level INTEGER NOT NULL,
    kills INTEGER NOT NULL,
    deaths INTEGER NOT NULL,
    assists INTEGER NOT NULL,
    credits INTEGER NOT NULL,
    PRIMARY KEY (match_id, username)
}

CREATE TABLE damage_breakdown{
    match_id INTEGER NOT NULL,
    win_loss VARCHAR(30) NOT NULL,
    username VARCHAR(30) NOT NULL,
    champion VARCHAR(30) NOT NULL,
    total_damage INTEGER NOT NULL,
    weapon_damage INTEGER NOT NULL,
    healing INTEGER NOT NULL,
    self_heal INTEGER NOT NULL,
    damage_taken INTEGER NOT NULL,
    shielding INTEGER NOT NULL,
    PRIMARY KEY (match_id, username)
}

CREATE TABLE player_data (
    match_id INTEGER NOT NULL,
    champion VARCHAR(30) NOT NULL,
    team_number INTEGER NOT NULL,
    username VARCHAR(30) NOT NULL,
    pick_number INTEGER NOT NULL,
    champ_level INTEGER NOT NULL,
    kills INTEGER NOT NULL,
    deaths INTEGER NOT NULL,
    assists INTEGER NOT NULL,
    credits INTEGER NOT NULL,
    win_loss VARCHAR(30) NOT NULL,
    total_damage INTEGER NOT NULL,
    weapon_damage INTEGER NOT NULL,
    healing INTEGER NOT NULL,
    self_heal INTEGER NOT NULL,
    damage_taken INTEGER NOT NULL,
    shielding INTEGER NOT NULL,
    PRIMARY KEY (match_id, champion)
);