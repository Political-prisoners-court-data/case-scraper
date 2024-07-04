CREATE USER airtable;
CREATE SCHEMA AUTHORIZATION airtable;

CREATE USER db;
GRANT USAGE ON SCHEMA scraper TO db;
GRANT TRUNCATE, SELECT ON ALL TABLES IN SCHEMA scraper TO db;

GRANT USAGE ON SCHEMA airtable TO db;
GRANT SELECT ON ALL TABLES IN SCHEMA airtable to db;

CREATE SCHEMA db;
GRANT USAGE ON SCHEMA db TO db;

CREATE TABLE db.rfm_person
(
    full_name  TEXT,
    aliases    text[],
    is_terr    boolean NOT NULL,
    birth_date date,
    address    text,
    PRIMARY KEY (full_name, birth_date)
);


GRANT TRUNCATE, SELECT, INSERT ON ALL TABLES IN SCHEMA db to db;

CREATE SCHEMA out;
GRANT USAGE ON SCHEMA out TO db;


CREATE TABLE out.rfm_person
(
    full_name  TEXT,
    aliases    text[],
    is_terr    boolean NOT NULL,
    birth_date date,
    address    text,
    PRIMARY KEY (full_name, birth_date)
);

-- CREATE TABLE out.rfm_added AS SELECT * FROM db.rfm_added;
CREATE TABLE out.rfm_added
(
    full_name  text,
    birth_date date,
    is_terr    boolean

);

-- CREATE TABLE out.rfm_removed AS SELECT * FROM db.rfm_removed;
create table out.rfm_removed
(
    full_name  text,
    birth_date date,
    is_terr    boolean
);

-- CREATE TABLE out.rfm_changed AS SELECT * FROM db.rfm_changed;
create table out.rfm_changed
(
    full_name   text,
    birth_date  date,
    old_is_terr boolean,
    new_is_terr boolean,
    old_aliases text[],
    new_aliases text[],
    old_address text,
    new_address text
);

GRANT TRUNCATE, SELECT, INSERT ON ALL TABLES IN SCHEMA out to db;

CREATE OR REPLACE VIEW db.rfm_added AS
SELECT new.full_name, new.birth_date, new.is_terr
FROM out.rfm_person AS old
         RIGHT OUTER JOIN db.rfm_person AS new
                          USING (full_name, birth_date)
WHERE old.full_name IS NULL;

CREATE OR REPLACE VIEW db.rfm_removed AS
SELECT old.full_name, old.birth_date, old.is_terr
FROM out.rfm_person AS old
         LEFT OUTER JOIN db.rfm_person AS new
                         USING (full_name, birth_date)
WHERE new.full_name IS NULL;

CREATE OR REPLACE VIEW db.rfm_changed AS
SELECT old.full_name,
       old.birth_date,
       old.is_terr as old_is_terr,
       new.is_terr as new_is_terr,
       old.aliases as old_aliases,
       new.aliases as new_aliases,
       old.address as old_address,
       new.address as new_address
FROM out.rfm_person AS old
         INNER JOIN db.rfm_person AS new
                    USING (full_name, birth_date)
WHERE old.is_terr <> new.is_terr
   OR old.address <> new.address
   OR old.aliases <> new.aliases;

CREATE VIEW out.match_rfm_full_name AS
SELECT *
FROM airtable.pzk
         INNER JOIN db.rfm_person
                    ON lower(name) = lower(full_name);


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


