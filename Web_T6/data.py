from datetime import datetime
from peewee import *
import uuid

db = SqliteDatabase('T6.db')


class User(Model):
    name = CharField()
    email = CharField()
    password = CharField()

    class Meta:
        database = db


class Secret(Model):
    s_id = AutoField()
    owner = ForeignKeyField(User, backref='secrets')
    title = CharField()
    description = TextField()
    money = FloatField()
    date_secret = DateField()
    place = CharField()
    lat = FloatField()
    lng = FloatField()

    class Meta:
        database = db


def generate_token():
    return str(uuid.uuid4()).replace('-', '')


def getDate(sDate: str):
    if "-" in sDate:
        withDash = int(sDate.split('-')[0])
        if withDash > 1000:
            resultDate = datetime.strptime(sDate, "%Y-%m-%d")
            return resultDate
        elif withDash <= 31:
            resultDate = datetime.strptime(sDate, "%d-%m-%Y")
            return resultDate

    elif "/" in sDate:
        withSlash = int(sDate.split('/')[0])
        if withSlash > 1000:
            resultDate = datetime.strptime(sDate, "%Y/%m/%d")
            return resultDate
        elif withSlash <= 31:
            resultDate = datetime.strptime(sDate, "%d/%m/%Y")
            return resultDate
