from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
import psycopg2

DATABASE_URL = "postgresql://postgres:xxx@localhost/NaturalDisaster"

class Database:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.metadata = MetaData(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def fetch_all_locations(self, table_name):
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        with self.engine.connect() as conn:
            query = select(table.c.location).distinct()
            result = conn.execute(query).fetchall()
        return [row['location'] for row in result]

    def count_events_by_location(self, table_name, location):
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        with self.engine.connect() as conn:
            query = select(table).where(table.c.location == location)
            result = conn.execute(query).fetchall()
        return len(result)

    def filter_data(self, table_name, column, value):
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        with self.engine.connect() as conn:
            query = select(table).where(table.c[column] == value)
            result = conn.execute(query).fetchall()
        return [dict(row) for row in result]