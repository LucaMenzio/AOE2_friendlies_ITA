from peewee import CharField, IntegerField
from models.db import BaseModel


class User(BaseModel):
    class Meta:
        table_name = 'users'

    name = CharField()
    profile_id = IntegerField()
    steam_id = CharField()
    discord_id = IntegerField(primary_key=True)

