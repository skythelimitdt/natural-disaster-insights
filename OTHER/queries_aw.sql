---total damage and deaths caused by classification type
SELECT 
    c."Disaster_Type", 
    SUM(a."Total_Deaths") AS "Total_Deaths", 
    SUM(d."Total_Damage_USD") AS "Total_Damage"
FROM 
    "classification" c
JOIN 
    "events" e 
ON 
    c."Classification_Key" = e."Classification_Key"
JOIN 
    "affected" a 
ON 
    e."ImpactID" = a."ImpactID"
JOIN 
    "damage" d 
ON 
    e."ImpactID" = d."ImpactID"
GROUP BY 
    c."Disaster_Type"
ORDER BY 
    "Total_Damage" DESC;

	
---from tropicalcyclone event name, total deaths, total affected, total damage
SELECT 
    t."Event_Name", 
    SUM(t."Total_Deaths") AS "Total_Deaths", 
    SUM(t."Total_Affected") AS "Total_Affected", 
    SUM(t."Total_Damage_USD") AS "Total_Damage"
FROM 
    "tropicalcyclone" t
GROUP BY 
    t."Event_Name"
ORDER BY 
    "Total_Damage" DESC;
	

---from tropicalcyclone see those impacted along with location impacted
SELECT 
    t."Event_Name", 
    t."ISO",
    a."Total_Deaths", 
    a."No_Injured",
    a."No_Affected",
    a."No_Homeless",
    a."Total_Affected",
	t."Location"
FROM 
    "tropicalcyclone" t
JOIN 
    "affected" a
ON
    t."DisNo" = a."DisNo"
GROUP BY 
    t."Event_Name", 
    t."Location", 
    t."ISO", 
    a."Total_Deaths", 
    a."No_Injured", 
    a."No_Affected", 
    a."No_Homeless", 
    a."Total_Affected"
ORDER BY 
    t."Event_Name" DESC;

---see the year event names began, the duration and the impact for each event
SELECT 
    d."Start_Year",
	e."duration",
    t."Event_Name",
    SUM(t."Total_Deaths") AS "Total_Deaths", 
    SUM(t."Total_Affected") AS "Total_Affected", 
    SUM(t."Total_Damage_USD") AS "Total_Damage"
FROM 
    "events" e
JOIN 
    "tropicalcyclone" t 
ON 
    e."DisNo" = t."DisNo"
JOIN 
    "damage" d
ON 
    e."DisNo" = d."DisNo"
GROUP BY 
    d."Start_Year", e."duration", t."Event_Name"
ORDER BY 
    d."Start_Year", "Total_Damage" DESC;

---top 5 Event Names sorted by total damage
SELECT 
    d."Start_Year",
    t."Event_Name", 
    d."ISO",
    c."Disaster_Type",
    c."Disaster_Subtype",
    d."Total_Damage_USD", 
    e."duration",
    t."Total_Deaths", 
    t."Total_Affected",
    a."Location"
FROM 
    "events" e
JOIN 
    "damage" d 
ON 
    e."ImpactID" = d."ImpactID"
JOIN 
    "tropicalcyclone" t 
ON 
    e."DisNo" = t."DisNo"
JOIN 
    "classification" c 
ON 
    e."Classification_Key" = c."Classification_Key"
JOIN 
    "affected" a
ON 
    e."ImpactID" = a."ImpactID"
WHERE 
    d."Start_Year" IS NOT NULL AND
    t."Event_Name" IS NOT NULL AND
    d."ISO" IS NOT NULL AND
    c."Disaster_Type" IS NOT NULL AND
    c."Disaster_Subtype" IS NOT NULL AND
    d."Total_Damage_USD" IS NOT NULL AND
    e."duration" IS NOT NULL AND
    t."Total_Deaths" IS NOT NULL AND
    t."Total_Affected" IS NOT NULL AND
    a."Location" IS NOT NULL
ORDER BY 
    d."Total_Damage_USD" DESC
LIMIT 5;

----What month and year has the highest # of events and the total cost in damage? 
---monthly analysis of events grouped by event count
SELECT 
    EXTRACT(YEAR FROM e."Start_Date") AS "Year", 
    EXTRACT(MONTH FROM e."Start_Date") AS "Month", 
    COUNT(e."DisNo") AS "Event_Count", 
    SUM(d."Total_Damage_USD") AS "Total_Damage"
FROM 
    "events" e
JOIN 
    "damage" d 
ON 
    e."ImpactID" = d."ImpactID"
GROUP BY 
    EXTRACT(YEAR FROM e."Start_Date"), 
    EXTRACT(MONTH FROM e."Start_Date")
ORDER BY 
    "Event_Count" DESC, "Total_Damage"; 

----what is the fatality count and total damage based on disaster type?
---total deaths and damage by disaster type
SELECT 
    c."Disaster_Type", 
    SUM(a."Total_Deaths") AS "Total_Deaths", 
    SUM(d."Total_Damage_USD") AS "Total_Damage"
FROM 
    "classification" c
JOIN 
    "events" e 
ON 
    c."Classification_Key" = e."Classification_Key"
JOIN 
    "affected" a 
ON 
    e."ImpactID" = a."ImpactID"
JOIN 
    "damage" d 
ON 
    e."ImpactID" = d."ImpactID"
GROUP BY 
    c."Disaster_Type"
ORDER BY 
    "Total_Deaths" DESC;

----What is the total persons affected listed in descending order?
---list total afected and include event name, disaster type and subgroup, total included, homeless, deaths and damage
SELECT 
    t."Event_Name", 
    c."Disaster_Type",
    c."Disaster_Subgroup",
    SUM(a."No_Injured") AS "Total_Injured", 
    SUM(a."No_Affected") AS "Total_Affected", 
    SUM(a."No_Homeless") AS "Total_Homeless",
    SUM(t."Total_Deaths") AS "Total_Deaths",
    SUM(t."Total_Damage_USD") AS "Total_Damage"
FROM 
    "events" e
JOIN 
    "affected" a 
ON 
    e."ImpactID" = a."ImpactID"
JOIN 
    "tropicalcyclone" t
ON 
    e."DisNo" = t."DisNo"
JOIN 
    "classification" c
ON
    e."Classification_Key" = c."Classification_Key"
GROUP BY 
    t."Event_Name", 
    c."Disaster_Type", 
    c."Disaster_Subgroup"
ORDER BY 
    "Total_Affected" DESC;




