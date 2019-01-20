DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS appointment;
DROP TABLE IF EXISTS reminder;
DROP TABLE IF EXISTS history;

CREATE TABLE IF NOT EXISTS user (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    email                 TEXT NOT NULL UNIQUE,
    name                  TEXT NOT NULL,
    password              TEXT NOT NULL,
    role                  TEXT NOT NULL,
    dob                   DATE,
    gender                TEXT,
    height                INTEGER DEFAULT 0,
    weight                INTEGER DEFAULT 0,
    fcode                 TEXT
);

CREATE TABLE IF NOT EXISTS reminder (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id               INTEGER REFERENCES user ON DELETE CASCADE,
    time                  TIME NOT NULL,
    medication            TEXT NOT NULL,
    quantity              TEXT
);

CREATE TABLE IF NOT EXISTS appointment (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id               INTEGER REFERENCES user ON DELETE CASCADE,
    date_time             TIMESTAMP NOT NULL,
    location              TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS history (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id               INTEGER REFERENCES user ON DELETE CASCADE,
    date                  DATE NOT NULL,
    description           TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS weather (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    last_update           TIMESTAMP,
    weather_text          TEXT,
    weather_icon          INTEGER,
    temperature           FLOAT,
    feel_temperature      FLOAT,
    humidity              INTEGER,
    wind_direction        INTEGER,
    wind_direction_text   TEXT,
    wind_speed            FLOAT,
    uv_index              INTEGER,
    uv_index_text         TEXT,
    visibility            FLOAT,
    cloud_cover           INTEGER,
    pressure              FLOAT,
    pressure_tendency     TEXT,
    dew_point             FLOAT
);

CREATE TABLE IF NOT EXISTS hospital (
  id                      TEXT PRIMARY KEY,
  last_update             DATE,
  name                    TEXT,
  address                 TEXT,
  lat                     FLOAT,
  lng                     FLOAT
);