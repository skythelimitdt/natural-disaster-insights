-- Total Damage on each year from latest year to oldest
SELECT 
	"Start_Year",
	SUM("Total_Damage_USD") AS total_damage
FROM damage
GROUP BY "Start_Year"
ORDER BY "Start_Year" DESC;

--Count the rows on each table
SELECT 
	COUNT("Classification_Key") AS row_count
FROM classification;

-- Perform an INNER JOIN on Damage and Classification tables
SELECT 
    d."Classification_Key", 
    c."Disaster_Group", 
    c."Disaster_Subgroup",
	d."Total_Damage_USD"
FROM 
    classification AS c
INNER JOIN 
    damage AS d 
ON 
    d."Classification_Key" = c."Classification_Key";