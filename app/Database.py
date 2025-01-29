from sqlalchemy import create_engine, MetaData, Table, select, func
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:121792@localhost/NaturalDisaster"

class Database:
    def __init__(self):
        # Initialize the database connection
        self.engine = create_engine(DATABASE_URL)
        self.metadata = MetaData(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        # Autoload tables to avoid redefining them repeatedly
        self.damage_table = Table("damage", self.metadata, autoload_with=self.engine)
        self.affected_table = Table("affected", self.metadata, autoload_with=self.engine)
        self.events_table = Table("events", self.metadata, autoload_with=self.engine)
        self.classification_table = Table("classification", self.metadata, autoload_with=self.engine)
        self.tropicalcyclone_table = Table("tropicalcyclone", self.metadata, autoload_with=self.engine)

    def fetch_all_event_types(self):
        # Fetch all disaster event types
        with self.engine.connect() as conn:
            query = select(self.classification_table.c.Disaster_Type.distinct())
            result = conn.execute(query).fetchall()
        return [row[0] for row in result]

    def fetch_all_locations(self):
        # Fetch all locations
        with self.engine.connect() as conn:
            query = (
                select(self.events_table.c.Location.distinct())
                .where(self.events_table.c.Start_Date >= self.start_date,
                       self.events_table.c.End_Date <= self.end_date)
            )
            result = conn.execute(query).fetchall()

        # Raise an error if no locations are found
        if not result:
            raise ValueError("No locations found for the given date range.")

        return [row[0] for row in result]
    
    def fetch_length_by_event_type(self, event_type):
        # Calculate the total duration of all events
        with self.engine.connect() as conn:
            query = (
                select(self.events_table.c.Start_Date, self.events_table.c.End_Date)
                .join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .where(self.classification_table.c.Disaster_Type == event_type)
            )
            result = conn.execute(query).fetchall()

        total_duration = 0
        for row in result:
            start_date, end_date = row[0], row[1]
            if start_date and end_date:
                total_duration += (end_date - start_date).days
        return total_duration

    def fetch_max_duration_by_event_type(self, event_type):
        # Fetch the maximum duration of events
        with self.engine.connect() as conn:
            query = (
                select(func.max(self.events_table.c.duration).label("max_duration"))
                .join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .where(self.classification_table.c.Disaster_Type == event_type)
                .where(self.events_table.c.duration.isnot(None))
            )
            result = conn.execute(query).scalar()
        return result or 0

    def fetch_min_duration_by_event_type(self, event_type):
        # Fetch the minimum duration of events
        with self.engine.connect() as conn:
            query = (
                select(func.min(self.events_table.c.duration).label("min_duration"))
                .join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .where(self.classification_table.c.Disaster_Type == event_type)
                .where(self.events_table.c.duration.isnot(None))
            )
            result = conn.execute(query).scalar()
        return result or 0

    def fetch_avg_duration_by_event_type(self, event_type):
        # Fetch the average duration of events
        with self.engine.connect() as conn:
            query = (
                select(func.avg(self.events_table.c.duration).label("avg_duration"))
                .join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .where(self.classification_table.c.Disaster_Type == event_type)
                .where(self.events_table.c.duration.isnot(None))
            )
            result = conn.execute(query).scalar()
        return result or 0

    def fetch_fatalities_by_event_type(self, event_type):
        # Calculate the total fatalities
        with self.engine.connect() as conn:
            query = (
                select(func.sum(self.affected_table.c.Total_Deaths).label("total_fatalities"))
                .join(self.events_table, self.affected_table.c.DisNo == self.events_table.c.DisNo)
                .join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .where(self.classification_table.c.Disaster_Type == event_type)
            )
            result = conn.execute(query).scalar()
        return result or 0
    
    def fetch_max_fatalities_by_event_type(self, event_type):
        # Fetch the max of fatalities
        with self.engine.connect() as conn:
            query = (
                select(func.max(self.affected_table.c.Total_Deaths).label("max_fatalities"))
                .join(self.events_table, self.affected_table.c.DisNo == self.events_table.c.DisNo)
                .join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .where(self.classification_table.c.Disaster_Type == event_type)
            )
            result = conn.execute(query).scalar()
        return result or 0

    def fetch_min_fatalities_by_event_type(self, event_type):
        # Fetch the min of fatalities
        with self.engine.connect() as conn:
            query = (
                select(func.min(self.affected_table.c.Total_Deaths).label("min_fatalities"))
                .join(self.events_table, self.affected_table.c.DisNo == self.events_table.c.DisNo)
                .join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .where(self.classification_table.c.Disaster_Type == event_type)
            )
            result = conn.execute(query).scalar()
        return result or 0

    def fetch_avg_fatalities_by_event_type(self, event_type):
        # Fetch the avg of fatalities
        with self.engine.connect() as conn:
            query = (
                select(func.avg(self.affected_table.c.Total_Deaths).label("avg_fatalities"))
                .join(self.events_table, self.affected_table.c.DisNo == self.events_table.c.DisNo)
                .join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .where(self.classification_table.c.Disaster_Type == event_type)
            )
            result = conn.execute(query).scalar()
        return result or 0

    def fetch_max_damages_by_event_type(self, event_type):
        # Fetch the maximum damages
        with self.engine.connect() as conn:
            query = (
                select(func.max(self.damage_table.c.Total_Damage_Adj_USD).label("max_damages"))
                .join(self.events_table, self.damage_table.c.DisNo == self.events_table.c.DisNo)
                .join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .where(self.classification_table.c.Disaster_Type == event_type)
            )
            result = conn.execute(query).scalar()
        return result or 0
    
    def fetch_min_damages_by_event_type(self, event_type):
        # Fetch the minimum damages
        with self.engine.connect() as conn:
            query = (
                select(func.min(self.damage_table.c.Total_Damage_Adj_USD).label("min_damages"))
                .join(self.events_table, self.damage_table.c.DisNo == self.events_table.c.DisNo)
                .join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .where(self.classification_table.c.Disaster_Type == event_type)
            )
            result = conn.execute(query).scalar()
        return result or 0

    def fetch_avg_damages_by_event_type(self, event_type):
        # Fetch the average damages
        with self.engine.connect() as conn:
            query = (
                select(func.avg(self.damage_table.c.Total_Damage_Adj_USD).label("avg_damages"))
                .join(self.events_table, self.damage_table.c.DisNo == self.events_table.c.DisNo)
                .join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .where(self.classification_table.c.Disaster_Type == event_type)
            )
            result = conn.execute(query).scalar()
        return result or 0
    
    def fetch_damage_by_event_type(self, event_type):
        # Fetch the total damages
        with self.engine.connect() as conn:
            query = (
                select(func.sum(self.damage_table.c.Total_Damage_Adj_USD).label("total_damages"))
                .join(self.events_table, self.damage_table.c.DisNo == self.events_table.c.DisNo)
                .join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .where(self.classification_table.c.Disaster_Type == event_type)
            )
            result = conn.execute(query).scalar()
        return result or 0

    def fetch_random_disaster(self):
        # Fetch a random disaster
        with self.engine.connect() as conn:
            query = (
                select(self.classification_table.c.Disaster_Type, self.classification_table.c.Disaster_Subtype)
                .join(self.events_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .order_by(func.random())
                .limit(1)
            )
            result = conn.execute(query).fetchone()
        return result
    
    def fetch_subtypes_by_event_type(self, event_type):
        with self.engine.connect() as conn:
            query = (
                select(self.classification_table.c.Disaster_Subtype.distinct())
                .where(self.classification_table.c.Disaster_Type == event_type)
            )
            result = conn.execute(query).fetchall()
        return [row[0] for row in result]

    def count_disasters_by_event_type_and_subtype(self, event_type, event_subtype):
        with self.engine.connect() as conn:
            query = (
                select(func.count().label("event_count"))
                .select_from(
                    self.classification_table.join(
                        self.events_table,
                        self.classification_table.c.Classification_Key == self.events_table.c.Classification_Key,
                    )
                )
                .where(self.classification_table.c.Disaster_Type == event_type)
            )
            if event_subtype:
                query = query.where(self.classification_table.c.Disaster_Subtype == event_subtype)
            result = conn.execute(query).scalar()
        return result or 0

    def search_location(self, location_name):
        # Search for disasters by location name, and only return the matching part of the location
        with self.engine.connect() as conn:
            query = (
                select(
                    self.events_table.c.Location,
                    self.events_table.c.Start_Date,
                    self.events_table.c.End_Date,
                    self.classification_table.c.Disaster_Group,
                    self.classification_table.c.Disaster_Subgroup,
                    self.classification_table.c.Disaster_Type,
                    self.classification_table.c.Disaster_Subtype
                )
                .join(
                    self.classification_table,
                    self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key,
                )
                .outerjoin(
                    self.damage_table,
                    self.events_table.c.DisNo == self.damage_table.c.DisNo,
                )
                .outerjoin(
                    self.affected_table,
                    self.events_table.c.DisNo == self.affected_table.c.DisNo,
                )
                .outerjoin(
                    self.tropicalcyclone_table,
                    self.events_table.c.DisNo == self.tropicalcyclone_table.c.DisNo,
                )
                .where(
                    self.events_table.c.Location.ilike(f'%{location_name}%') |
                    self.affected_table.c.Location.ilike(f'%{location_name}%') |
                    self.tropicalcyclone_table.c.Location.ilike(f'%{location_name}%')
                )
            )
            result = conn.execute(query).fetchall()
            return result

    def search_year(self, year):
        # Search for disasters by year
        with self.engine.connect() as conn:
            query = (
                select(
                    self.events_table.c.Location,
                    self.events_table.c.Start_Date,
                    self.events_table.c.End_Date,
                    self.classification_table.c.Disaster_Group,
                    self.classification_table.c.Disaster_Subgroup,
                    self.classification_table.c.Disaster_Type,
                    self.classification_table.c.Disaster_Subtype
                )
                .join(
                    self.classification_table,
                    self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key,
                )
                .where(
                    self.events_table.c.Start_Date <= f"{year}-12-31",
                    self.events_table.c.End_Date >= f"{year}-01-01"
                )
            )
            result = conn.execute(query).fetchall()

        return [dict(row) for row in result]

