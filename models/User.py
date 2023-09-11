from peewee import CharField, IntegerField
from models.db import BaseModel


class User(BaseModel):
    class Meta:
        table_name = 'users'

    id = IntegerField(primary_key=True)
    name = CharField()


