from dataclasses import fields
from datetime import datetime, time

import pytz
from pymongo import MongoClient
from sqlalchemy import create_engine, text

from demhack8.items import RfmPersonItem


class PersonEventGenerator:

    def __init__(self, connection, mongo_client):
        self.__connection = connection
        self.__mongo_client = mongo_client

    def generate(self):
        added_result = self.__connection.execute(text('SELECT * FROM rfm_added'))
        changed_result = self.__connection.execute(text('SELECT * FROM rfm_changed'))
        removed_result = self.__connection.execute(text('SELECT * FROM rfm_removed'))

        field_names = [self.__to_camel_case(field.name) for field in fields(RfmPersonItem)]
        result_list = []

        for changed_row_mapping in changed_result.mappings():
            changed_event = {self.__to_camel_case(key): val
                             for (key, val) in changed_row_mapping.items()
                             if val is not None}
            self.__fullfill_common_fields(changed_event, 'changed')
            result_list.append(changed_event)

        for row_vals in added_result.tuples():
            add_event = dict(zip(field_names, row_vals))
            add_event = {k: v for (k, v) in add_event.items() if v is not None}
            self.__fullfill_common_fields(add_event, 'added')
            result_list.append(add_event)

        for row_vals in removed_result.tuples():
            removed_event = dict(zip(field_names, row_vals))
            removed_event = {k: v for (k, v) in removed_event.items() if v is not None}
            self.__fullfill_common_fields(removed_event, 'removed')
            result_list.append(removed_event)

        db = self.__mongo_client['eventsDb']
        collection = db['events']

        if result_list:
            collection.insert_many(result_list, ordered=False)

        self.__mongo_client.close()

    def __fullfill_common_fields(self, event: dict, action: str):
        if event['birthDate']:
            event['birthDate'] = datetime.combine(event['birthDate'], time.min)
        event['action'] = action
        event['date'] = datetime.now(pytz.UTC)

    @staticmethod
    def __to_camel_case(str):
        name = ''.join(str.title().split('_'))
        return name[0].lower() + name[1:]


if __name__ == '__main__':
    engine = create_engine('postgresql://db@localhost:5432/postgres')
    with engine.begin() as connection:
        gen = PersonEventGenerator(connection, MongoClient())
        gen.generate()
        connection.commit()
