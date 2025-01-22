-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.
DROP TABLE "Damage";
DROP TABLE "Classification" CASCADE;
DROP TABLE "Locations" CASCADE;
DROP TABLE "Events" CASCADE;
DROP TABLE "Affected" CASCADE;

CREATE TABLE "Damage" (
    "ImpactID" VARCHAR(255)   NOT NULL,
    "DisNo" VARCHAR(255)   NOT NULL,
    "Classification_Key" VARCHAR(100)   NOT NULL,
    "LocationID" VARCHAR(255)   NOT NULL,
    "ISO" VARCHAR(3)   NOT NULL,
    "Start_Year" INTEGER   NOT NULL,
    "Total_Damage_USD" FLOAT   NULL,
    "Total_Damage_Adj_USD" FLOAT   NULL,
    CONSTRAINT "pk_Damage" PRIMARY KEY (
        "ImpactID"
     )
);

CREATE TABLE "Affected" (
    "ImpactID" VARCHAR(255)   NOT NULL,
    "LocationID" VARCHAR(255)   NOT NULL,
    "Classification_Key" VARCHAR(100)   NOT NULL,
    "ISO" VARCHAR(3)   NOT NULL,
    "Total_Deaths" FLOAT   NULL,
    "No_Injured" FLOAT   NULL,
    "No_Affected" FLOAT   NULL,
    "No_Homeless" FLOAT   NULL,
    "Total_Affected" FLOAT   NULL,
    CONSTRAINT "pk_Affected" PRIMARY KEY (
        "ImpactID"
     )
);

CREATE TABLE "Events" (
    "DisNo" VARCHAR(255)   NOT NULL,
    "ImpactID" VARCHAR(255)   NOT NULL,
    "Historic" VARCHAR(250)   NOT NULL,
    "Classification_Key" VARCHAR(100)   NOT NULL,
    "Disaster_Group" VARCHAR(255)   NOT NULL,
    "Disaster_Subgroup" VARCHAR(255)   NOT NULL,
    "Disaster_Type" VARCHAR(255)   NOT NULL,
    "Disaster_Subtype" VARCHAR(255)   NOT NULL,
    "Event_Name" VARCHAR(255)   NULL,
    "OFDA_BHA_Response" VARCHAR(3)   NOT NULL,
    "Appeal" VARCHAR(3)   NOT NULL,
    "Declaration" VARCHAR(3)   NOT NULL,
    "Origin" VARCHAR(255)   NULL,
    "Associated_Types" VARCHAR(255)   NULL,
    "Magnitude" FLOAT   NULL,
    "Magnitude_Scale" VARCHAR(255)   NULL,
    "Start_Date" DATE   NOT NULL,
    "End_Date" DATE   NOT NULL,
    "duration" INTEGER   NOT NULL,
    CONSTRAINT "pk_Events" PRIMARY KEY (
        "DisNo"
     ),
    CONSTRAINT "uc_Events_ImpactID" UNIQUE (
        "ImpactID"
    )
);

CREATE TABLE "Locations" (
    "LocationID" VARCHAR(255)   NOT NULL,
    "DisNo" VARCHAR(255)   NOT NULL,
    "Classification_Key" VARCHAR(100)   NOT NULL,
    "ISO" VARCHAR(3)   NOT NULL,
    "Country" VARCHAR(255)   NOT NULL,
    "Subregion" VARCHAR(255)   NOT NULL,
    "Region" VARCHAR(255)   NOT NULL,
    "Location" VARCHAR(3000)   NULL,
    "Latitude" FLOAT   NULL,
    "Longitude" FLOAT   NULL,
    "River_Basin" VARCHAR(500)   NULL,
    CONSTRAINT "pk_Locations" PRIMARY KEY (
        "LocationID"
     ),
    CONSTRAINT "uc_Locations_DisNo" UNIQUE (
        "DisNo"
    )
);

CREATE TABLE "Classification" (
    "Classification_Key" VARCHAR(100)   NOT NULL,
    "Disaster_Group" VARCHAR(255)   NOT NULL,
    "Disaster_Subgroup" VARCHAR(255)   NOT NULL,
    "Disaster_Type" VARCHAR(255)   NOT NULL,
    "Disaster_Subtype" VARCHAR(255)   NOT NULL,
    CONSTRAINT "pk_Classification" PRIMARY KEY (
        "Classification_Key"
     )
);

SELECT * FROM "Affected";

ALTER TABLE "Damage" ADD CONSTRAINT "fk_Damage_Classification_Key" FOREIGN KEY("Classification_Key")
REFERENCES "Classification" ("Classification_Key");

ALTER TABLE "Damage" ADD CONSTRAINT "fk_Damage_LocationID" FOREIGN KEY("LocationID")
REFERENCES "Locations" ("LocationID");

ALTER TABLE "Affected" ADD CONSTRAINT "fk_Affected_LocationID" FOREIGN KEY("LocationID")
REFERENCES "Locations" ("LocationID");

ALTER TABLE "Affected" ADD CONSTRAINT "fk_Affected_Classification_Key" FOREIGN KEY("Classification_Key")
REFERENCES "Classification" ("Classification_Key");

ALTER TABLE "Events" ADD CONSTRAINT "fk_Events_ImpactID" FOREIGN KEY("ImpactID")
REFERENCES "Affected" ("ImpactID");

ALTER TABLE "Events" ADD CONSTRAINT "fk_Events_Classification_Key" FOREIGN KEY("Classification_Key")
REFERENCES "Classification" ("Classification_Key");

ALTER TABLE "Locations" ADD CONSTRAINT "fk_Locations_DisNo" FOREIGN KEY("DisNo")
REFERENCES "Events" ("DisNo");

ALTER TABLE "Locations" ADD CONSTRAINT "fk_Locations_Classification_Key" FOREIGN KEY("Classification_Key")
REFERENCES "Classification" ("Classification_Key");

