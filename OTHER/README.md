# natural-disaster-insights

## Overview
In this project we focused on designing our program using the dataset: The International Disaster Database from: The Centre for Research on the Epidemiology of Disasters (CRED). This dataset contains compiled information on natural disasters from 1900 to the current date. We worked to display this data in a user-accessable and searchable format. The user can access the data through various inputs such as county, address, and disaster type. The program will display information for the search results that shows the number of fatalities for a given disaster. 

To clean and organize the data we created an ETL Workflow and stored the clean data in PostgreSQL. To manage our reading data we made a Flask API with JSON output. The libraries we used are: Chart.js, D3.js, Plotly, Pygubu, and Tkinter. Using these in tandem with Flask we designed apps for visualization. 



## Technologies Used
- Python  
- PostgreSQL  
- Chart.js  
- D3.js  
- Flask  
- JSON  
- Plotly  
- Pygubu  
- Tkinter  



## File Structure
- resources - Contains the input files and transformed CSV files  
- data - Python Database  
- ui - App data and UI  
- logic\ - App controller  



## Data Ethics Considerations
- Dataset used is Open Access. Sourced from: The Centre for Research on the Epidemiology of Disasters (CRED)



## Data Engineering Track
**For this track, your group will follow data engineering processes. Here are the specific requirements:**
- Data must be stored in a SQL or NoSQL database (PostgreSQL, MongoDB, SQLite, etc) and the database must include at least two tables (SQL) or collections (NoSQL).
- The database must contain at least 100 records.
- Your project must use ETL workflows to ingest data into the database (i.e. the data should not be exactly the same as the original source; it should have been transformed in some way).
- Your project must include a method for reading data from the database and displaying it for future use, such as:
    - Pandas DataFrame
    - Flask API with JSON output   

*Your project must use one additional library not covered in class related to data engineering. Consider libraries for data streaming, cloud, data pipelines, or data validation.*



**Your GitHub repo must include a README.md with an outline of the project including:**
- An overview of the project and its purpose
- Instructions on how to use and interact with the project
- Documentation of the database used and why (e.g. benefits of SQL or NoSQL for this project)
- ETL workflow with diagrams or ERD
- At least one paragraph summarizing efforts for ethical considerations made in the project
- References for the data source(s)
- References for any code used that is not your own


*OPTIONAL: add user-driven interaction, either before or after the ETL process. e.g.:*
*- BEFORE: provide a menu of options for the user to narrow the range of data being extracted from a data source (e.g. API or CSV file, where fields are known in advance).*
*- AFTER: Once the data is stored in the database, add user capability to extract filtered data from the database prior to loading it in a Pandas DataFrame or a JSON output from a Flask API.*



## Resources and Support
- ASU Bootcamp class activities
- Xpert Learning Assistant
- ChatGPT
- The International Disaster Database - Centre for Research on the Epidemiology of Disasters (CRED)
