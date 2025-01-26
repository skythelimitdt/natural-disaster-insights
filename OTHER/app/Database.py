from sqlalchemy import create_engine, MetaData, Table, select, func, extract, and_
from sqlalchemy.orm import sessionmaker

###Ian's setup
##DATABASE_URL = "postgresql://postgres:121792@localhost/NaturalDisaster"

###Angelina's setup
DATABASE_URL = "postgresql://postgres:postgres@localhost/natural_disasters"

class Database:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.metadata = MetaData()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        # # Define the date range for 2000s filtering
        # self.start_date = "2000-01-01"
        # ##update to 2024-12-31
        # self.end_date = "2024-12-31"

        # Autoload tables to avoid redefining them each time
        self.damage_table = Table("damage", self.metadata, autoload_with=self.engine)
        self.affected_table = Table("affected", self.metadata, autoload_with=self.engine)
        self.events_table = Table("events", self.metadata, autoload_with=self.engine)
        self.classification_table = Table("classification", self.metadata, autoload_with=self.engine)
        self.tropicalcyclone_table = Table("tropicalcyclone", self.metadata, autoload_with=self.engine)

    def fetch_all_event_types(self):
        with self.engine.connect() as conn:
            query = select(self.classification_table.c.Disaster_Type.distinct())
            result = conn.execute(query).fetchall()
        return [row[0] for row in result]

    def count_disasters_by_event_type(self, event_type):
        with self.engine.connect() as conn:
            query = (
                select(func.count(self.events_table.c.DisNo))
                .join(
                    self.classification_table,
                    self.events_table.c.Classification_Key == self.classification_table.c.Classification_Key
                )
                .where(self.classification_table.c.Disaster_Type == event_type)
            )
            result = conn.execute(query).scalar()
        return result
  
    def count_disasters_by_event_type(self, event_type):
        """Count disasters by a given event type."""
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
            result = conn.execute(query).scalar()
        return result or 0

def search_events_by_year(self, year):
    """Search disasters within a specific year."""
    with self.engine.connect() as conn:
        query = (
            select(
                self.events_table.c.Start_Date,
                self.events_table.c.End_Date,
                self.events_table.c.Origin,
                self.events_table.c.Magnitude,
            )
            .where(func.date_part('year', self.events_table.c.Start_Date) == year)
            .where(self.events_table.c.Start_Date.isnot(None))  # Ensure Start_Date is not NULL
        )
        result = conn.execute(query).fetchall()
    return [dict(row) for row in result]

def monthly_analysis(self):
    """Run a monthly analysis of events."""
    with self.engine.connect() as conn:
        query = (
            select(
                func.date_part('year', self.events_table.c.Start_Date).label("Year"),
                func.date_part('month', self.events_table.c.Start_Date).label("Month"),
                func.count(self.events_table.c.DisNo).label("Event_Count"),
                func.sum(self.damage_table.c.Total_Damage_USD).label("Total_Damage"),
            )
            .select_from(
                self.events_table.join(
                    self.damage_table,
                    self.events_table.c.ImpactID == self.damage_table.c.ImpactID
                )
            )
            .where(self.events_table.c.Start_Date.isnot(None))  # Exclude NULL Start_Date values
            .group_by(
                func.date_part('year', self.events_table.c.Start_Date),
                func.date_part('month', self.events_table.c.Start_Date),
            )
            .order_by(
                func.count(self.events_table.c.DisNo).desc(),
                func.sum(self.damage_table.c.Total_Damage_USD).desc(),
            )
        )
        result = conn.execute(query).fetchall()
    return [dict(row) for row in result]
    
    # def fetch_all_locations(self):
    #     with self.engine.connect() as conn:
    #         query = (
    #             select(self.locations_table.c.Location)
    #             .distinct()
    #             .join(self.tropicalcyclone_table, self.locations_table.c.LocationID == self.tropicalcyclone_table.c.LocationID)
    #             .join(self.events_table, self.tropicalcyclone_table.c.DisNo == self.events_table.c.DisNo)
    #             .where(
    #                 self.events_table.c.Start_Date >= self.start_date,
    #                 self.events_table.c.End_Date <= self.end_date
    #             )
    #         )
    #         result = conn.execute(query).fetchall()

    #     # Check if result is empty
    #     if not result:
    #         raise ValueError("No locations found for the given date range.")

    #     # Return the locations
    #     return [row[0] for row in result]
    
    # def count_events_by_location(self, location_name):
    #     with self.engine.connect() as conn:
    #         query = (
    #             select([self.locations_table.c.Location, func.count(self.events_table.c.DisNo).label('event_count')])
    #             .join(self.tropicalcyclone_table, self.locations_table.c.LocationID == self.tropicalcyclone_table.c.LocationID)
    #             .join(self.events_table, self.tropicalcyclone_table.c.DisNo == self.events_table.c.DisNo)
    #             .where(self.locations_table.c.Location == location_name)
    #             .group_by(self.locations_table.c.Location)
    #         )
    #         result = conn.execute(query).fetchone()

    #     if result:
    #         return result['event_count']
    #     else:
    #         raise ValueError(f"No events found for the location: {location_name}")

    def search_year(self, events, classification, year):
        if year < 2000 or year > 2010:
            raise ValueError("The year must be between 2000 and 2010.")

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
                    events_table.c.End_Date >= f"{year}-01-01",
                    events_table.c.Start_Date >= "2000-01-01",
                    events_table.c.End_Date <= "2010-12-31",
                )
            )
            result = conn.execute(query).fetchall()

        return [dict(row) for row in result]