#!/usr/bin/env python

import pandas as pd
from pyairtable import Api
from sqlalchemy import create_engine

engine = create_engine("postgresql://airtable@localhost:5432/postgres")

api = Api('patoCRTkfxdzWWT0Y.f20c7fccca48bbbbffe5d1d993f8415ebc5fd3b2d95b4a15ab38e590dc949202')
pzk = pd.json_normalize(api.table('app1sDXWAmADet7vo', 'tbl321Qu3l3aQfvYp').all())
pzk.rename(columns={
    'id': 'id',
    'createdTime': 'created_time',
    'fields.++ФИО': 'name',
    'fields.Дело': 'case',
    'fields.Регион': 'region',
    'fields.++Город': 'town',
    'fields.Возраст': 'age',
    'fields.Росфинмониторинг': 'rfm',
    'fields.Дата включения в список РФМ': 'date_rfm_added',
    'fields.Дата исключения из списка РФМ': 'date_rfm_removed'
}, inplace=True)
pzk = pzk.convert_dtypes()
pzk.date_rfm_added = pd.to_datetime(pzk.date_rfm_added)
pzk.date_rfm_removed = pd.to_datetime(pzk.date_rfm_removed)
pzk.created_time = pd.to_datetime(pzk.created_time)
pzk.set_index('id', inplace=True)
print(pzk.head())
with engine.begin() as connection:
    print(pzk.to_sql('pzk', connection, if_exists='replace'))
