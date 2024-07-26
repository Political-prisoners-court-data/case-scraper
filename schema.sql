CREATE USER db;

CREATE SCHEMA AUTHORIZATION scraper;
GRANT USAGE ON SCHEMA scraper TO db;
GRANT TRUNCATE, SELECT ON ALL TABLES IN SCHEMA scraper TO db;

CREATE TABLE scraper.rfm_person
(
    full_name TEXT,
    aliases text[],
    is_terr boolean NOT NULL,
    birth_date date,
    address text,
    PRIMARY KEY (full_name, birth_date)
);


CREATE SCHEMA db;
GRANT USAGE ON SCHEMA db TO db;
GRANT TRUNCATE, SELECT, INSERT ON ALL TABLES IN SCHEMA db to db;

CREATE TABLE db.rfm_person
(
    full_name  TEXT,
    aliases    text[],
    is_terr    boolean NOT NULL,
    birth_date date,
    address    text,
    PRIMARY KEY (full_name, birth_date)
);


CREATE SCHEMA out;
GRANT USAGE ON SCHEMA out TO db;
GRANT TRUNCATE, SELECT, INSERT ON ALL TABLES IN SCHEMA out to db;

CREATE TABLE out.rfm_person
(
    full_name  TEXT,
    aliases    text[],
    is_terr    boolean NOT NULL,
    birth_date date,
    address    text,
    PRIMARY KEY (full_name, birth_date)
);

CREATE OR REPLACE VIEW db.rfm_added AS
SELECT new.full_name,
       new.aliases,
       new.is_terr,
       new.birth_date,
       new.address
FROM out.rfm_person AS old
         RIGHT OUTER JOIN db.rfm_person AS new
                          USING (full_name, birth_date)
WHERE old.full_name IS NULL;

CREATE OR REPLACE VIEW db.rfm_removed AS
SELECT old.full_name,
       old.aliases,
       old.is_terr,
       old.birth_date,
       old.address
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


CREATE USER airtable;
CREATE SCHEMA AUTHORIZATION airtable;
GRANT USAGE ON SCHEMA airtable TO db;
GRANT SELECT ON ALL TABLES IN SCHEMA airtable to db;

CREATE VIEW out.match_rfm_full_name AS
SELECT *
FROM airtable.pzk
         INNER JOIN db.rfm_person
                    ON lower(name) = lower(full_name);
