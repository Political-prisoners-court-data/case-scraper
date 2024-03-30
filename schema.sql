CREATE USER scraper;

CREATE SCHEMA AUTHORIZATION scraper

CREATE TABLE rfm_person
(
    full_name TEXT,
    aliases text[],
    is_terr boolean NOT NULL,
    birth_date date,
    address text,
    PRIMARY KEY (full_name, birth_date)
);


