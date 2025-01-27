-- Total Damage on each year from latest year to oldest
SELECT 
	"Start_Year",
	SUM("Total_Damage_USD") AS total_damage
FROM "Damage"
GROUP BY "Start_Year"
ORDER BY "Start_Year" DESC;

--Count the rows on each table
SELECT 
	COUNT("Classification_Key") AS row_count
FROM "Classification";

-- Perform an INNER JOIN on Damage and Classification tables
SELECT 
    d."Classification_Key", 
    c."Disaster_Group", 
    c."Disaster_Subgroup",
	d."Total_Damage_USD"
FROM 
    "Classification" AS c
INNER JOIN 
    "Damage" AS d 
ON 
    d."Classification_Key" = c."Classification_Key";