# Natural Disasters Between 2000-2024

## Contributors
- Angelina Wright
- Eylem Yildirim
- Ian O'Connor
- Lily Saltonstall
  
## Project Overview
In this project we focused on designing our program using the dataset: The International Disaster Database from: The Centre for Research on the Epidemiology of Disasters (CRED). This dataset contains compiled information on natural disasters from 2000 to 2024. 

### Data Collection

### ETL Process

### Database Setup
The database was set up using PostgreSQL. Given the smaller dataset size, PostgreSQL was deemed more suitable than MongoDB for this project. 
[quickdatabasediagrams.com](quickdatabasediagrams.com) is used to create different tables and define the relationships between them. schema.sql file was downloaded to create the tables in the database in PgAdmin. 

![ERD]( 

### Web Application


## To Run the app
- Clone the Repo
- Pull the files
- Create database in PgAmin as "NaturalDisaster"
- Run schema.sql for the database to create the tables
- Import files to each table
- Update database.py file with your login credentials
- Run the app in the terminal: python main.py

## Tech Stack and Data Flow
We used a number of different libraries/tools/resources for this project, including:
- Python
- Jupyter Notebook
- Pandas
- Hashlib
- PostgreSQL  
- Tkinter
- PIL
- SQLAlchemy

Natural Disasters Dataset: [https://public.emdat.be/data] (https://public.emdat.be/data)


## Data Ethics Considerations
- Dataset used is Open Access. Sourced from: The Centre for Research on the Epidemiology of Disasters (CRED)












## Resources and Support
- ASU Bootcamp class activities
- Xpert Learning Assistant
- ChatGPT
- The International Disaster Database - Centre for Research on the Epidemiology of Disasters (CRED)
