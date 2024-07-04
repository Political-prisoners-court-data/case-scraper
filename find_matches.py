#!/usr/bin/env python

import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("postgresql://db@localhost:5432/postgres")
with engine.begin() as conn:
    conn.execute(text)

    pzk = pd.read_sql('SELECT * FROM airtable.pzk;', conn, index_col='id').drop(columns='created_time')
    rfm = pd.read_sql('SELECT * FROM db.rfm_person;', conn)
print(pzk.head())
print(rfm.head())
