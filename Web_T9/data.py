from datetime import datetime
from peewee import *
import math

db = SqliteDatabase('T9.db')


class Bill(Model):
    bill_id = AutoField()
    client_name = CharField()
    rnc = CharField()
    b_date = DateField()
    description = TextField()

    class Meta:
        database = db


class Product(Model):
    product_id = AutoField()
    code = CharField()
    name = CharField()
    price = FloatField()

    class Meta:
        database = db


class Bill_Detail(Model):
    id_detail = AutoField()
    id_bill = ForeignKeyField(Bill, backref='detail')
    id_product = ForeignKeyField(Product, backref='items')
    quantity = IntegerField()
    t_value = FloatField()

    class Meta:
        database = db


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


def counting(b_id: int):
    subt = 0
    query_subt = Bill_Detail.select().join(Bill).where(Bill.bill_id == b_id)
    for u in query_subt:
        subt += u.t_value
    itbis = round(subt * 0.16, 2)
    total = round(subt + itbis, 2)
    return {'subt': subt, 'itbis': itbis, 'total': total}


def getDetails(b_id: int):
    details = []
    for d in Bill_Detail.select().join(Bill).where(Bill.bill_id == b_id):
        detail = {
            "id_detail": d.id_detail,
            "prod_code": d.id_product.code,
            "prod_name": d.id_product.name,
            "unit_price": d.id_product.price,
            "cant": d.quantity,
            "tvalue": d.t_value
        }
        details.append(detail)
    return details


def serverAnswer(status: bool, msg: str, args={}):
    _arg = False
    if args != {}:
        _arg = True
    a = {'ok': status, 'msg': msg, 'arg': args}
    b = {'ok': status, 'msg': msg}
    return a if _arg else b
