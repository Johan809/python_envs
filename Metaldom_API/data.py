import os
import io
import zipfile
from peewee import *
from datetime import datetime
from fastapi.responses import Response

db = SqliteDatabase('Metaldom.db')


class DBModel(Model):
    class Meta:
        database = db


class User(DBModel):
    _id = AutoField()
    username = CharField()
    name = CharField()
    email = CharField()
    pwd = CharField()
    is_dev = BooleanField()


class Request(DBModel):
    _id = AutoField()
    id_client = ForeignKeyField(User, backref='client')
    request_type = CharField()
    description = CharField()
    creation_date = DateField()
    was_attended = BooleanField()


class Request_Answer(DBModel):
    _id = AutoField()
    id_request = ForeignKeyField(Request, backref='request')
    id_dev = ForeignKeyField(User, backref='dev')
    meet_link = CharField()
    comment = CharField()


class Evaluation(DBModel):
    _id = AutoField()
    id_request = ForeignKeyField(Request, backref='request')
    id_answer = ForeignKeyField(Request_Answer, backref='answer')
    description = CharField()
    investment_return = FloatField()


class C_Resume(DBModel):
    _id = AutoField()
    id_eva = ForeignKeyField(Evaluation, backref='evaluation')
    description = CharField()
    value = FloatField()


class Files(DBModel):
    _id = AutoField()
    id_eva = ForeignKeyField(Evaluation, backref='evaluation')
    uri = TextField()


def getResume(_id: int):
    try:
        resume = []
        for re in C_Resume.select().join(Evaluation).where(Evaluation._id == _id):
            one_re = {
                'description': re.description,
                'value': re.value
            }
            resume.append(one_re)
        return resume
    except:
        return []

def getFiles(_id: int):
    try:
        all_files = []
        for f in Files.select().join(Evaluation).where(Evaluation._id == _id):
            one_file = {
                'id': f._id,
                'uri': f.uri
            }
            all_files.append(one_file)
        return all_files
    except:
        return []


def getLastEvaID():
    try:
        last = Evaluation.select().order_by(Evaluation._id.desc()).get()
        lastID = last._id
        return lastID + 1
    except:
        return 1

def getTotal(_id: int):
    try:
        total = 0
        for re in C_Resume.select().join(Evaluation).where(Evaluation._id == _id):
            total += re.value
        return total
    except:
        return 0


def getDate(_date: str):
    if "-" in _date:
        withDash = int(_date.split('-')[0])
        if withDash > 1000:
            resultDate = datetime.strptime(_date, "%Y-%m-%d")
            return resultDate
        elif withDash <= 31:
            resultDate = datetime.strptime(_date, "%d-%m-%Y")
            return resultDate

    elif "/" in _date:
        withSlash = int(_date.split('/')[0])
        if withSlash > 1000:
            resultDate = datetime.strptime(_date, "%Y/%m/%d")
            return resultDate
        elif withSlash <= 31:
            resultDate = datetime.strptime(_date, "%d/%m/%Y")
            return resultDate


def zipfiles(filenames: list):
    s = io.BytesIO()
    zf = zipfile.ZipFile(s, "w")
    zip_filename = "archive.zip"

    for fpath in filenames:
        fdir, fname = os.path.split(fpath)
        zf.write(fpath, fname)
    zf.close()

    resp = Response(s.getvalue(), media_type="application/x-zip-compressed", headers={
        'Content-Disposition': f'attachment;filename={zip_filename}'
    })
    return resp


def serverAnswer(status: bool, msg: str, args={}):
    _arg = False
    if args != {}:
        _arg = True
    a = {'ok': status, 'msg': msg, 'arg': args}
    b = {'ok': status, 'msg': msg}
    return a if _arg else b
