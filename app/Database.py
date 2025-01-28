from sqlalchemy import create_engine, MetaData, Table, select, func
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:121792@localhost/NaturalDisaster"

class Database:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.metadata = MetaData(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        # Autoload tables to avoid redefining them repeatetively
        self.damage_table = Table("damage", self.metadata, autoload_with=self.engine)
        self.affected_table = Table("affected", self.metadata, autoload_with=self.engine)
        self.locations_table = Table("locations", self.metadata, autoload_with=self.engine)
        self.events_table = Table("events", self.metadata, autoload_with=self.engine)
        self.classification_table = Table("classification", self.metadata, autoload_with=self.engine)
        self.tropicalcyclone_table = Table("tropicalcyclone", self.metadata, autoload_with=self.engine)

    def fetch_all_event_types(self):
        with self.engine.connect() as conn:
            query = select(self.classification_table.c.Disaster_Type.distinct())
            result = conn.execute(query).fetchall()
        return [row[0] for row in result]

    def fetch_all_locations(self):
        with self.engine.connect() as conn:
            query = (
                select(self.locations_table.c.Location)
                .distinct()
                .join(self.tropicalcyclone_table, self.locations_table.c.LocationID == self.tropicalcyclone_table.c.LocationID)
                .join(self.events_table, self.tropicalcyclone_table.c.DisNo == self.events_table.c.DisNo)
                .where(
                    self.events_table.c.Start_Date >= self.start_date,
                    self.events_table.c.End_Date <= self.end_date
                )
            )
            result = conn.execute(query).fetchall()

        # Check if result is empty
        if not result:
            raise ValueError("No locations found for the given date range.")

        # Return locations
        return [row[0] for row in result]
    
    def fetch_length_by_event_type(self, event_type):
        with self.engine.connect() as conn:
            query = (
                select(self.events_table.c.Start_Date, self.events_table.c.End_Date)
                .join(self.classification_table)
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
        with self.engine.connect() as conn:
            query = (
                select(func.max(self.events_table.c.End_Date - self.events_table.c.Start_Date).label("max_duration"))
                .join(self.classification_table)
                .where(self.classification_table.c.Disaster_Type == event_type)
            )
            result = conn.execute(query).scalar()
        return result or 0

    def fetch_min_duration_by_event_type(self, event_type):
        with self.engine.connect() as conn:
            query = (
                select(func.min(self.events_table.c.End_Date - self.events_table.c.Start_Date).label("min_duration"))
                .join(self.classification_table)
                .where(self.classification_table.c.Disaster_Type == event_type)
            )
            result = conn.execute(query).scalar()
        return result or 0

    def fetch_avg_duration_by_event_type(self, event_type):
        with self.engine.connect() as conn:
            query = (
                select(func.avg(self.events_table.c.End_Date - self.events_table.c.Start_Date).label("avg_duration"))
                .join(self.classification_table)
                .where(self.classification_table.c.Disaster_Type == event_type)
            )
            result = conn.execute(query).scalar()
        return result or 0

    def fetch_fatalities_by_event_type(self, event_type):
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
        """Fetch the maximum damages for the given event type."""
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
        """Fetch the minimum damages for the given event type."""
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
        """Fetch the average damages for the given event type."""
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
        with self.engine.connect() as conn:
            query = select(self.classification_table.c.Disaster_Type, self.classification_table.c.Disaster_Subtype).\
            join(self.events_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key).\
            order_by(func.random()).limit(1)
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
    
    def count_events_by_location(self, location_name):
        with self.engine.connect() as conn:
            query = (
                select([self.locations_table.c.Location, func.count(self.events_table.c.DisNo).label('event_count')])
                .join(self.tropicalcyclone_table, self.locations_table.c.LocationID == self.tropicalcyclone_table.c.LocationID)
                .join(self.events_table, self.tropicalcyclone_table.c.DisNo == self.events_table.c.DisNo)
                .where(self.locations_table.c.Location == location_name)
                .group_by(self.locations_table.c.Location)
            )
            result = conn.execute(query).fetchone()

        if result:
            return result['event_count']
        else:
            raise ValueError(f"No events found for the location: {location_name}")
    
    def search_location(self, location_name):
        with self.engine.connect() as conn:
            query = (
                select(
                    self.events_table.c.Origin,
                    self.events_table.c.Magnitude,
                    self.events_table.c.Start_Date,
                    self.events_table.c.End_Date,
                    self.classification_table.c.Disaster_Group,
                    self.classification_table.c.Disaster_Subgroup,
                    self.classification_table.c.Disaster_Type,
                    self.classification_table.c.Disaster_Subtype,
                )
                .join(
                    self.classification_table,
                    self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key,
                )
                .join(
                    self.tropicalcyclone_table,
                    self.events_table.c.DisNo == self.tropicalcyclone_table.c.DisNo,
                )
                .join(
                    self.locations_table,
                    self.tropicalcyclone_table.c.LocationID == self.locations_table.c.LocationID,
                )
                .where(self.locations_table.c.Location.ilike(f'%{location_name}%'))  # Search using the location name with wildcard
            )
            result = conn.execute(query).fetchall()

        return [dict(row) for row in result]

    def search_year(self, events, classification, year):

        events_table = Table(events, self.metadata, autoload_with=self.engine)
        classification_table = Table(classification, self.metadata, autoload_with=self.engine)

        with self.engine.connect() as conn:
            query = (
                select(
                    events_table.c.Origin,
                    events_table.c.Magnitude,
                    events_table.c.Start_Date,
                    events_table.c.End_Date,
                    classification_table.c.Disaster_Group,
                    classification_table.c.Disaster_Subgroup,
                    classification_table.c.Disaster_Type,
                    classification_table.c.Disaster_Subtype,
                )
                .join(
                    classification_table,
                    events_table.c.Classification_Key == classification_table.c.Classification_Key,
                )
                .where(
                    events_table.c.Start_Date <= f"{year}-12-31",
                    events_table.c.End_Date >= f"{year}-01-01"
                )
            )
            result = conn.execute(query).fetchall()

        return [dict(row) for row in result]

