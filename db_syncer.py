dbconfig = {
    "dbname": 'CafeDB',
    "user": 'postgres',
    "password": 'sepibzyr79',
    "host": 'localhost',
    "port": '5432'
}

config = ' '.join([key + '=' + value for key, value in dbconfig.items()])
