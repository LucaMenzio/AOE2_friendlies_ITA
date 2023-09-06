from peewee import Model, MySQLDatabase
from dotenv import load_dotenv
import os
load_dotenv()

MYSQL_ENDPOINT = os.getenv('MYSQL_ENDPOINT')
MYSQL_USERNAME = os.getenv('MYSQL_USERNAME')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

db = MySQLDatabase(database=MYSQL_DATABASE,
                   host=MYSQL_ENDPOINT,
                   port=3306,
                   user=MYSQL_USERNAME,
                   password=MYSQL_PASSWORD)

db.init(MYSQL_DATABASE)


class BaseModel(Model):
    class Meta:
        database = db

