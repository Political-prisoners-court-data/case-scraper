from itemadapter import ItemAdapter
from sqlalchemy import create_engine, insert, table, column


class SqlAlchemyPipeline:
    def __init__(self, engine_uri):
        self.engine = create_engine(engine_uri)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(engine_uri=crawler.settings.get("SQL_ENGINE_URI"))

    def process_item(self, item, spider):
        if hasattr(item.__class__, 'table'):
            table_name = getattr(item.__class__, 'table')
            columns = [column(f) for f in ItemAdapter(item).keys()]
            t = table(table_name, *columns)
            with self.engine.begin() as connection:
                connection.execute(insert(t).values(**ItemAdapter(item)))
        return item
