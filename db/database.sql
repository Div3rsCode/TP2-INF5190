create table arrondissement(
    id  INTEGER PRIMARY KEY,
    nom VARCHAR(50) NOT NULL UNIQUE
);


create table piscine(
    id              INTEGER PRIMARY KEY,
    id_uev          INTEGER,
    arrondissement  VARCHAR(50),
    nom_installation VARCHAR(50),
    type_installation VARCHAR(50),
    adresse         VARCHAR(50),
    propriete       VARCHAR(50),
    gestion         VARCHAR(50),
    point_x         REAL,
    point_y         REAL,    
    equipement     VARCHAR(50),
    longitude       REAL,
    latitude        REAL
);


create table patinoire(
    id                  INTEGER PRIMARY KEY,
    arrondissement      VARCHAR(50),
    nom_installation    VARCHAR(50),
    date_maj            DATETIME,
    ouvert              BOOLEAN,
    deblaye             BOOLEAN,
    arrose              BOOLEAN,
    resurface           BOOLEAN
);


create table glissade(
    id                  INTEGER PRIMARY KEY,
    nom_installation    VARCHAR(50),    
    arrondissement      VARCHAR(50),
    code_arr            varchar(3),
    date_maj            DATETIME,
    ouvert              BOOLEAN,
    deblaye             BOOLEAN,
    condition           VARCHAR(50)
);



