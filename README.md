# tait-stats
displaying skills in SQL, psycopg2 and pandas by storing stats from a csv file to a postgresql database, then fetching data and performing analysis.

## Usage:

1. ensure you have a (preferrably virtual) python environment containing pandas and psycopg2, and you are using postgreSQL.
2. run setup_params.sh and enter the name of db you want to store the data in and your postgres password.
3. you can now run any part of the code. running setupTables.py creates the stats and fixtures tables in your db and initialises with data from the csv files.

## IMPORTANT
Once setup_params.sh has been run, params.ini will contain the db name and your password. 
If you wish to keep these on file, you can add params.ini to your .gitignore file, else run reset_params.sh to remove db name and password.


##Database Strucure

![statsSchema](https://user-images.githubusercontent.com/78791293/192114575-e62a35fc-2901-42b6-adbe-e5aa19b79a77.png)

This structure is used as long term it will allow me to add data from different seasons, teams and formats.
With the previous structure this would not have been possible. Using a snowflake schema.
