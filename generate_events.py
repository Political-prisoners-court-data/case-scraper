from dataclasses import fields
from datetime import datetime

import pytz
from pymongo import MongoClient
from sqlalchemy import create_engine, text

from demhack8.items import RfmPersonItem


class PersonEventGenerator:

    def __init__(self, sql_engine, mongo_client):
        self._sql_engine = sql_engine
        self._mongo_client = mongo_client

    def generate(self):
        with self._sql_engine.begin() as connection:
            added_result = connection.execute(text('SELECT * FROM rfm_added'))
            changed_result = connection.execute(text('SELECT * FROM rfm_changed'))
            removed_result = connection.execute(text('SELECT * FROM rfm_removed'))
            connection.commit()

        field_names = [self.__to_camel_case(field.name) for field in fields(RfmPersonItem)]
        field_names.append('action')
        field_names.append('date')

        added_list = [dict(zip(field_names, (tuple(row_vals._tuple()) + ('added', datetime.now(pytz.UTC),)))) for
                      row_vals in added_result]
        changed_list = []
        removed_list = [dict(zip(field_names, (tuple(row_vals._tuple()) + ('removed', datetime.now(pytz.UTC),)))) for
                        row_vals in removed_result]

        for changed_row_mapping in changed_result.mappings():
            changed_dict_row = {self.__to_camel_case(key): val for (key, val) in changed_row_mapping.items()}
            changed_dict_row['birthDate'] = datetime.combine(changed_dict_row['birthDate'], datetime.min.time())
            changed_dict_row['action'] = 'changed'
            changed_dict_row['date'] = datetime.now(pytz.UTC)
            changed_list.append(changed_dict_row)

        for person_dict in added_list:
            person_dict['birthDate'] = datetime.combine(person_dict['birthDate'], datetime.min.time())

        for person_dict in removed_list:
            person_dict['birthDate'] = datetime.combine(person_dict['birthDate'], datetime.min.time())

        db = self._mongo_client['events']
        collection = db['events']

        collection.insert_many(added_list, ordered=False)
        collection.insert_many(changed_list, ordered=False)
        collection.insert_many(removed_list, ordered=False)

        self._mongo_client.close()

    @staticmethod
    def __to_camel_case(str):
        name = ''.join(str.title().split('_'))
        return name[0].lower() + name[1:]


if __name__ == '__main__':
    engine = create_engine('postgresql://db@localhost:5432/postgres')
    gen = PersonEventGenerator(engine, MongoClient())
    gen.generate()
