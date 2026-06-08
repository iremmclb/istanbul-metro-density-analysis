<<<<<<< HEAD
--to clean the dataset from non-rail system data

DELETE FROM passenger_flow 
WHERE StationId IS NULL; -- the StationId of bus data is null.

DELETE FROM passenger_flow 
WHERE LineId LIKE '34%'; -- all LineId of metrobus data start with 34.

DELETE FROM transferLine 
WHERE Id = 97; -- Id = 97 is a teleferic line 

DELETE FROM stations 
WHERE LineName LIKE 'TF%'; -- teleferic lines
=======
--to clean the dataset from non-rail system data

DELETE FROM passenger_flow 
WHERE StationId IS NULL; -- the StationId of bus data is null.

DELETE FROM passenger_flow 
WHERE LineId LIKE '34%'; -- all LineId of metrobus data start with 34.

DELETE FROM transferLine 
WHERE Id = 97; -- Id = 97 is a teleferic line 

DELETE FROM stations 
WHERE LineName LIKE 'TF%'; -- teleferic lines
>>>>>>> 9de07c3eb3d672793e370d965da2856ac1283bc3
