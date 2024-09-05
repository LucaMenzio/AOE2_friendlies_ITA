from mysql.connector import connect, Error
import os
from dotenv import load_dotenv

load_dotenv()
MYSQL_ENDPOINT = os.getenv('MYSQL_ENDPOINT')
MYSQL_USERNAME = os.getenv('MYSQL_USERNAME')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

try:
    with connect(
        host = MYSQL_ENDPOINT,
        user = MYSQL_USERNAME,
        password = MYSQL_PASSWORD,
        database = MYSQL_DATABASE,
    ) as connection:

        query = "select * from test"

        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor:
            print(row)
except Error as e:
    print(e)