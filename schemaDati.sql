CREATE TABLE ardere (
    idardere INTEGER PRIMARY KEY
                     UNIQUE
                     NOT NULL,
    idbosco  INT,
    data     DATE,
    quintali REAL,
    prezzo   REAL,
    totale   REAL,
    note     TEXT
);

CREATE TABLE bosco (
    idbosco         INTEGER      PRIMARY KEY
                                 NOT NULL
                                 UNIQUE,
    idproprietario  INT,
    luogo           VARCHAR (25),
    mappale         TEXT,
    denuncia_taglio TEXT,
    data_denuncia   DATE,
    prezzomc        REAL,
    prezzoq         REAL,
    forfait         REAL,
    corteccia       INTEGER      DEFAULT (0),
    venditamc       REAL         DEFAULT (0)
);

CREATE TABLE ore_lavoro (
    idore       INTEGER PRIMARY KEY
                        UNIQUE
                        NOT NULL,
    idbosco     INT,
    data        DATE,
    numero_ore  REAL,
    prezzo_uni  REAL,
    tipo_lavoro VARCHAR,
    totale      REAL,
    note        VARCHAR
);

CREATE TABLE proprietario (
    idproprietario INTEGER      PRIMARY KEY
                                NOT NULL
                                UNIQUE,
    cognome        VARCHAR (25),
    nome           VARCHAR (25),
    citta          TEXT,
    indirizzo      TEXT,
    numero         TEXT,
    provincia      VARCHAR (2),
    tel            TEXT
);

CREATE TABLE spesa (
    idspesa    INTEGER PRIMARY KEY
                       UNIQUE
                       NOT NULL,
    idbosco    INT,
    data       DATE,
    tipo       TEXT,
    prezzo_uni REAL,
    unita      INT,
    totale     REAL,
    note       TEXT
);

CREATE TABLE tronco (
    idtronco   INTEGER PRIMARY KEY
                       NOT NULL
                       UNIQUE,
    idbosco    INT,
    specie     TEXT,
    placchetta INT     NOT NULL,
    lunghezza  REAL    NOT NULL,
    diametro   REAL    NOT NULL,
    mc         REAL
);
