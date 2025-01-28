DROP TABLE damage CASCADE;
DROP TABLE classification CASCADE;
DROP TABLE events CASCADE;
DROP TABLE affected CASCADE;
DROP TABLE tropicalcyclone CASCADE;

CREATE TABLE "damage" (
    "ImpactID" VARCHAR(255)   NOT NULL,
    "DisNo" VARCHAR(255)   NOT NULL,
    "Classification_Key" VARCHAR(100)   NOT NULL,
    "Location" VARCHAR(3000)   NULL,
    "ISO" VARCHAR(3)   NOT NULL,
    "Start_Year" INTEGER   NOT NULL,
    "Total_Damage_USD" FLOAT   NULL,
    "Total_Damage_Adj_USD" FLOAT   NULL,
    CONSTRAINT "pk_damage" PRIMARY KEY (
        "ImpactID"
     )
);

CREATE TABLE "affected" (
    "ImpactID" VARCHAR(255)   NOT NULL,
    "Classification_Key" VARCHAR(100)   NOT NULL,
    "DisNo" VARCHAR(255)   NOT NULL,
    "ISO" VARCHAR(3)   NOT NULL,
    "Total_Deaths" FLOAT   NULL,
    "No_Injured" FLOAT   NULL,
    "No_Affected" FLOAT   NULL,
    "No_Homeless" FLOAT   NULL,
    "Total_Affected" FLOAT   NULL,
    "Location" VARCHAR(3000)   NULL,
    CONSTRAINT "pk_affected" PRIMARY KEY (
        "ImpactID"
     )
);

CREATE TABLE "events" (
    "DisNo" VARCHAR(255)   NOT NULL,
    "ImpactID" VARCHAR(255)   NOT NULL,
    "Historic" VARCHAR(250)   NOT NULL,
    "Classification_Key" VARCHAR(100)   NOT NULL,
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
    "Location" VARCHAR(3000)   NULL,
    CONSTRAINT "pk_events" PRIMARY KEY (
        "DisNo"
     )
);

CREATE TABLE "classification" (
    "Classification_Key" VARCHAR(100)   NOT NULL,
    "Disaster_Group" VARCHAR(255)   NOT NULL,
    "Disaster_Subgroup" VARCHAR(255)   NOT NULL,
    "Disaster_Type" VARCHAR(255)   NOT NULL,
    "Disaster_Subtype" VARCHAR(255)   NOT NULL,
    CONSTRAINT "pk_classification" PRIMARY KEY (
        "Classification_Key"
     )
);

CREATE TABLE "tropicalcyclone" (
    "DisNo" VARCHAR(255)   NOT NULL,
    "ImpactID" VARCHAR(255)   NOT NULL,
    "Location" VARCHAR(3000)   NULL,
    "Classification_Key" VARCHAR(100)   NOT NULL,
    "Event_Name" VARCHAR(255)   NOT NULL,
    "ISO" VARCHAR(3)   NOT NULL,
    "Total_Deaths" FLOAT   NULL,
    "Total_Affected" FLOAT   NULL,
    "Start_Date" DATE   NOT NULL,
    "Total_Damage_USD" FLOAT   NULL,
    "Total_Damage_Adj_USD" FLOAT   NULL,
    "duration" INTEGER   NOT NULL,
    CONSTRAINT "pk_tropicalcyclone" PRIMARY KEY (
        "ImpactID"
     ),
    CONSTRAINT "uc_tropicalcyclone_DisNo" UNIQUE (
        "DisNo"
    )
);

ALTER TABLE "damage" ADD CONSTRAINT "fk_damage_Classification_Key" FOREIGN KEY("Classification_Key")
REFERENCES "classification" ("Classification_Key");

ALTER TABLE "affected" ADD CONSTRAINT "fk_affected_Classification_Key" FOREIGN KEY("Classification_Key")
REFERENCES "classification" ("Classification_Key");

ALTER TABLE "affected" ADD CONSTRAINT "fk_affected_DisNo" FOREIGN KEY("DisNo")
REFERENCES "events" ("DisNo");

ALTER TABLE "events" ADD CONSTRAINT "fk_events_ImpactID" FOREIGN KEY("ImpactID")
REFERENCES "damage" ("ImpactID");

ALTER TABLE "events" ADD CONSTRAINT "fk_events_Classification_Key" FOREIGN KEY("Classification_Key")
REFERENCES "classification" ("Classification_Key");

ALTER TABLE "tropicalcyclone" ADD CONSTRAINT "fk_tropicalcyclone_DisNo" FOREIGN KEY("DisNo")
REFERENCES "events" ("DisNo");

