#!/usr/bin/env python

from sqlalchemy import create_engine, text

engine = create_engine('postgresql://db@localhost:5432/postgres')

with engine.begin() as connection:
    connection.execute(text('TRUNCATE TABLE out.rfm_added'))
    connection.execute(text('TRUNCATE TABLE out.rfm_removed'))
    connection.execute(text('TRUNCATE TABLE out.rfm_changed'))
    connection.execute(text('TRUNCATE TABLE out.rfm_person'))
    connection.execute(text('INSERT INTO out.rfm_added SELECT * from db.rfm_added'))
    connection.execute(text('INSERT INTO out.rfm_removed SELECT * from db.rfm_removed'))
    connection.execute(text('INSERT INTO out.rfm_changed SELECT * from db.rfm_changed'))
    connection.execute(text('INSERT INTO out.rfm_person SELECT * from db.rfm_person'))
    connection.execute(text('TRUNCATE TABLE db.rfm_person'))
    connection.execute(text('INSERT INTO db.rfm_person SELECT * from scraper.rfm_person'))
    connection.execute(text('TRUNCATE TABLE scraper.rfm_person'))
    connection.commit()
