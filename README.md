# Natural Disasters Between 2000-2024

## Contributors
- Angelina Wright
- Eylem Yildirim
- Ian O'Connor
- Lily Saltonstall
  
## Project Overview
In this project we focused on designing our program using data from the Emergency Events Database created by a joint initiative between The Centre for Research on the Epidemiology of Disasters (CRED) and the World Health Organization (WHO). This dataset contains compiled information on natural disasters in North America from 2000 to 2024. 

### Data Collection
Data was collected from EM-DAT Data for Natural Disasters: https://public.emdat.be/data

### ETL Process

- Extract
    - Data was was downloaded as an Excel .xlsx file obtained from [EM-DAT The International Disaster Databse](https://www.emdat.be/)

- Transform 
    - Data Transforamtion
        - Calculated event duration in days by adding `Duration` column and calculating the difference between `Start_Date` and `End_Date`
        -  Using `hashlib` library, created column to uniquely identify `ImpactID`
    - Data Cleaning
        - Dropped columns containing null values: `AID Contribution ('000 US$)`, `Reconstruction Costs ('000 US$)`, `Reconstruction Costs, Adjusted ('000 US$)`
        - Removed rows with null values in End Month, Start Day, and End Day columns 
        - Checked and dropped duplicate values
        - Renamed column names to simplify data querying 
        - Removed single quotes from `Event_Name` column 
        - Filtered `Event_Name` to retain only events categorized under the `Disaster_Subtype` of `Tropical Cyclone`, and dropped rows related to other events
    -  DataFrames Creation

- Load
  - Exported cleaned and transformed DataFrames as CSV files for use in downstream application, PostgreSQL



### Database Setup
The database was set up using PostgreSQL. Given the smaller dataset size, PostgreSQL was deemed more suitable than MongoDB for this project. 
[quickdatabasediagrams.com](quickdatabasediagrams.com) is used to create different tables and define the relationships between them. schema.sql file was downloaded to create the tables in the database in PgAdmin.5 tables were created:

![ERD](https://github.com/skythelimitdt/natural-disaster-insights/blob/main/resources/ERD/ERD%20image.png)

### GUI Application

NaturalDisasterApp
│
├── main.py

├── AppController.py

├── Splash.py

├── Menu.py

├── Database.py

├── SearchLocation.py

├── SearchYear.py

├── DeadlyEvent.py

├── DestructiveEvent.py

├── CountEvent.py

├── RandomEvent.py

├── EventLength.py

├── EventImage.py

└── InputValidation.py


## To Run the app
- Clone the [repository](https://github.com/skythelimitdt/natural-disaster-insights) from GitHub to your local machine
- Set up the Database
    - Open pgAdmin and create a database named `NaturalDisaster`
    - Run `schema.sql` in the database to create the tables
- Import Data
    Import the provided CSV files in the `resources` folder
- Update Databse Credentials
    - Edit the `Database.py` file with your pgAdmin login details
- Run the App
    - In the terminal, navigate to the folder with `main.py` and run:
```python
python main.py 
```

## Tech Stack and Data Flow
We used a number of different libraries/tools/resources for this project, including:
- Python
- Jupyter Notebook
- Pandas
- Hashlib
- PostgreSQL  
- Tkinter
- PIL (Python Imaging Library)
- SQLAlchemy




## Data Ethics Considerations
- Dataset used is Open Access. Sourced from: The Centre for Research on the Epidemiology of Disasters (CRED)












## Resources and Support
- ASU/OSU Bootcamp class activities
- Xpert Learning Assistant
- ChatGPT
    - Asked for assistance in identifying a Python library for generating unique values. ChatGPT suggested the hashlib library, which was used in creating the `ImpactID`. It also assisted in formulating the code logic to concatenate key columns and generate unique, consistent identifiers for each row. This helped ensure data integrity and avoid duplicate entries.
- The International Disaster Database - Centre for Research on the Epidemiology of Disasters (CRED)
