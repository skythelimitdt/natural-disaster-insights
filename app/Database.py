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
    
    def fetch_length_by_event_type(self, event_type, event_subtype=None):
        with self.engine.connect() as conn:
            query = (
                select(func.sum(self.events_table.c.duration))
                .join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .where(self.classification_table.c.Disaster_Type == event_type)
                .where(self.events_table.c.duration.isnot(None))
            )
            if event_subtype:
                query = query.where(self.classification_table.c.Disaster_Subtype == event_subtype)

            result = conn.execute(query).scalar()
        return result if result else 0

    def fetch_max_duration_by_event_type(self, event_type, event_subtype=None):
        with self.engine.connect() as conn:
            query = (
                select(func.max(self.events_table.c.duration).label("max_duration"))
                .join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .where(self.classification_table.c.Disaster_Type == event_type)
                .where(self.events_table.c.duration.isnot(None))
            )
            if event_subtype:
                query = query.where(self.classification_table.c.Disaster_Subtype == event_subtype)

            result = conn.execute(query).scalar()
            
            # Ensure that the returned value is a valid number
            if result is not None and isinstance(result, (int, float)):
                return result
            return 0

    def fetch_min_duration_by_event_type(self, event_type, event_subtype=None):
        # Fetch the minimum duration of events
        with self.engine.connect() as conn:
            query = (
                select(func.min(self.events_table.c.duration).label("min_duration"))
                .join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .where(self.classification_table.c.Disaster_Type == event_type)
                .where(self.events_table.c.duration.isnot(None))
            )
            if event_subtype:
                query = query.where(self.classification_table.c.Disaster_Subtype == event_subtype)

            result = conn.execute(query).scalar()
            
            # Ensure that the returned value is a valid number
            if result is not None and isinstance(result, (int, float)):
                return result
            return 0

    def fetch_avg_duration_by_event_type(self, event_type, event_subtype=None):
        with self.engine.connect() as conn:
            query = (
                select(func.avg(self.events_table.c.duration).label("avg_duration"))
                .join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .where(self.classification_table.c.Disaster_Type == event_type)
                .where(self.events_table.c.duration.isnot(None))
            )
            if event_subtype:
                query = query.where(self.classification_table.c.Disaster_Subtype == event_subtype)

            result = conn.execute(query).scalar()
            
            return result if result is not None else 0

    def fetch_fatalities_by_event_type(self, event_type, event_subtype=None):
        # Calculate the total fatalities
        with self.engine.connect() as conn:
            query = (
                select(func.sum(self.affected_table.c.Total_Deaths).label("total_fatalities"))
                .join(self.events_table, self.affected_table.c.DisNo == self.events_table.c.DisNo)
                .join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .where(self.classification_table.c.Disaster_Type == event_type)
            )
            if event_subtype:
                query = query.where(self.classification_table.c.Disaster_Subtype == event_subtype)

            result = conn.execute(query).scalar()
        return result or 0
    
    def fetch_max_fatalities_by_event_type(self, event_type, event_subtype=None):
        # Fetch the max of fatalities
        with self.engine.connect() as conn:
            query = (
                select(func.max(self.affected_table.c.Total_Deaths).label("max_fatalities"))
                .join(self.events_table, self.affected_table.c.DisNo == self.events_table.c.DisNo)
                .join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .where(self.classification_table.c.Disaster_Type == event_type)
            )
            if event_subtype:
                query = query.where(self.classification_table.c.Disaster_Subtype == event_subtype)

            result = conn.execute(query).scalar()
        return result or 0

    def fetch_min_fatalities_by_event_type(self, event_type, event_subtype=None):
        # Fetch the min of fatalities
        with self.engine.connect() as conn:
            query = (
                select(func.min(self.affected_table.c.Total_Deaths).label("min_fatalities"))
                .join(self.events_table, self.affected_table.c.DisNo == self.events_table.c.DisNo)
                .join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .where(self.classification_table.c.Disaster_Type == event_type)
            )
            if event_subtype:
                query = query.where(self.classification_table.c.Disaster_Subtype == event_subtype)

            result = conn.execute(query).scalar()
        return result or 0

    def fetch_max_damages_by_event_type(self, event_type, event_subtype=None):
        # Fetch the maximum damages
        with self.engine.connect() as conn:
            query = (
                select(func.max(self.damage_table.c.Total_Damage_Adj_USD).label("max_damages"))
                .join(self.events_table, self.damage_table.c.DisNo == self.events_table.c.DisNo)
                .join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .where(self.classification_table.c.Disaster_Type == event_type)
            )
            if event_subtype:
                query = query.where(self.classification_table.c.Disaster_Subtype == event_subtype)

            result = conn.execute(query).scalar()
        return result or 0
    
    def fetch_min_damages_by_event_type(self, event_type, event_subtype=None):
        # Fetch the minimum damages
        with self.engine.connect() as conn:
            query = (
                select(func.min(self.damage_table.c.Total_Damage_Adj_USD).label("min_damages"))
                .join(self.events_table, self.damage_table.c.DisNo == self.events_table.c.DisNo)
                .join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .where(self.classification_table.c.Disaster_Type == event_type)
            )
            if event_subtype:
                query = query.where(self.classification_table.c.Disaster_Subtype == event_subtype)

            result = conn.execute(query).scalar()
        return result or 0

    def fetch_avg_damages_by_event_type(self, event_type, event_subtype=None):
        # Fetch the average damages
        with self.engine.connect() as conn:
            query = (
                select(func.avg(self.damage_table.c.Total_Damage_Adj_USD).label("avg_damages"))
                .join(self.events_table, self.damage_table.c.DisNo == self.events_table.c.DisNo)
                .join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                .where(self.classification_table.c.Disaster_Type == event_type)
            )
            if event_subtype:
                query = query.where(self.classification_table.c.Disaster_Subtype == event_subtype)

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
    
    def fetch_subtypes_by_event_type(self, event_type):
        with self.engine.connect() as conn:
            query = (
                select(self.classification_table.c.Disaster_Subtype.distinct())
                .where(self.classification_table.c.Disaster_Type == event_type)
            )
            result = conn.execute(query).fetchall()
        return [row[0] for row in result]

    def count_disasters_by_event_type_and_subtype(self, event_type=None, event_subtype=None):
        with self.engine.connect() as conn:
            query = select(func.count()).select_from(self.events_table)

            if event_type:
                query = query.join(self.classification_table, self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key)
                query = query.where(self.classification_table.c.Disaster_Type == event_type)

            if event_subtype:
                query = query.where(self.classification_table.c.Disaster_Subtype == event_subtype)

            result = conn.execute(query).scalar()
        
        return result or 0

    def search_location(self, location_name):
        # Search for disasters by location
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

