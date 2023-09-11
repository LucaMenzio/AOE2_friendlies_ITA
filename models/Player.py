from peewee import CharField, IntegerField, ForeignKeyField
from models.db import BaseModel
from models.User import User


class Player(BaseModel):
    class Meta:
        table_name = 'players'

    name = CharField()
    profile_id = IntegerField(primary_key=True)
    steam_id = CharField()
    user_id = IntegerField(null=True)

    user = ForeignKeyField(User, backref='players', null=True)

