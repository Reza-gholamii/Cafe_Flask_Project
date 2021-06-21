from core.configs import *


dbconfig = {
    "dbname": 'cafedb',
    "user": 'postgres',
    "password": 'sepibzyr79',
    "host": 'localhost',
    "port": '5432'
}

config = " ".join([f"{key}={dbconfig[key]}" for key in dbconfig.keys()])

# creating tables
with DataBaseContext(dbconfig) as DBCursor:
    for query in sql_queries:
        DBCursor.execute(query)
