#!/usr/bin/env python
from pymongo import MongoClient
from sqlalchemy import create_engine, text
from generate_events import PersonEventGenerator

engine = create_engine('postgresql://db@localhost:5432/postgres')

with engine.begin() as connection:
    scraper_result = connection.execute(text('SELECT COUNT(*) FROM scraper.rfm_person')).scalar()
    db_result = connection.execute(text('SELECT COUNT(*) FROM db.rfm_person')).scalar()

    if scraper_result > 0:  # Prevent every person truncation for unsuccessful scraping
        connection.execute(text('TRUNCATE TABLE out.rfm_person'))
        connection.execute(text('INSERT INTO out.rfm_person SELECT * from db.rfm_person'))
        connection.execute(text('TRUNCATE TABLE db.rfm_person'))
        connection.execute(text('INSERT INTO db.rfm_person SELECT * from scraper.rfm_person'))
        connection.execute(text('TRUNCATE TABLE scraper.rfm_person'))

        if db_result > 0:  # Ignore every person 'added' events generation for first start
            generator = PersonEventGenerator(connection=connection, mongo_client=MongoClient())
            generator.generate()

    connection.commit()
