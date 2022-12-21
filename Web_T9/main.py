from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from peewee import *
from data import *

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:4200",
    "http://localhost:8100"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
db.connect()
db.create_tables([Bill, Product, Bill_Detail], safe=True)


class BillModel(BaseModel):
    client_name: str
    rnc: str
    b_date: str
    des: str


class ProductModel(BaseModel):
    code: str
    name: str
    price: float


class BDetail_Model(BaseModel):
    id_b: int
    id_p: int
    quantity: int


@app.get('/')
def index():
    products = []
    bills = []
    details = []
    for p in Product.select():
        product = {
            'p_id': p.product_id,
            'code': p.code,
            'name': p.name,
            'price': p.price
        }
        products.append(product)
    for b in Bill.select():
        bill = {
            'id': b.bill_id,
            'client': b.client_name,
            'rnc': b.rnc,
            'date': b.b_date,
            'des': b.description
        }
        bills.append(bill)
    for d in Bill_Detail.select():
        detail = {
            'id': d.id_detail,
            'idF': d.id_bill,
            'idP': d.id_product,
            'cant': d.quantity,
            'tprice': d.t_value
        }
        details.append(detail)
    return{'bills': bills, 'details': details, 'products': products}


@app.post('/bills/create')
def bills_create(bill: BillModel):
    try:
        _date = getDate(bill.b_date)
        newBill = Bill(client_name=bill.client_name, rnc=bill.rnc,
                       b_date=_date, description=bill.des)
        newBill.save()
        return serverAnswer(True, 'Factura agregada con exito', {'id': newBill.bill_id})
    except:
        return serverAnswer(False, "Error en bd")


@app.post('/product')
def product_create(prod: ProductModel):
    try:
        newProd = Product(code=prod.code, name=prod.name, price=prod.price)
        newProd.save()
        return serverAnswer(True, 'Producto agregado')
    except:
        return serverAnswer(False, "Error en bd")


@app.post('/detail/create')
def add_detail(det: BDetail_Model):
    value = 0
    try:
        actual_bill = Bill.get(Bill.bill_id == det.id_b)
        actual_prod = Product.get(Product.product_id == det.id_p)
        query = Product.select().where(Product.product_id == det.id_p)
        for p in query:
            value = p.price * det.quantity
        newDetail = Bill_Detail(
            id_bill=actual_bill, id_product=actual_prod, quantity=det.quantity, t_value=value)
        newDetail.save()
        msg = f"Detalle de la factura con ID: {det.id_b} agregada con exito"
        return serverAnswer(True, msg, newDetail.id_detail)
    except:
        return serverAnswer(False, "Error en bd")


@app.get('/bills/read')
def bills_read():
    bills = []
    try:
        for b in Bill.select():
            calcs = counting(b.bill_id)
            bill = {
                'id': b.bill_id,
                'client': b.client_name,
                'rnc': b.rnc,
                'date': b.b_date,
                'descrip': b.description,
                'details': getDetails(b.bill_id),
                'subt': calcs['subt'],
                'itbis': calcs['itbis'],
                'total': calcs['total']
            }
            bills.append(bill)
        return serverAnswer(True, 'Todas las facturas guardadas', {'Facturas': bills})
    except:
        return serverAnswer(False, "Error de busqueda")


@app.get('/bills/read/{b_id}')
def bill_read(b_id: int):
    try:
        for b in Bill.select().where(Bill.bill_id == b_id):
            calcs = counting(b.bill_id)
            bill = {
                'id': b.bill_id,
                'client': b.client_name,
                'rnc': b.rnc,
                'date': b.b_date,
                'descrip': b.description,
                'details': getDetails(b.bill_id),
                'subt': calcs['subt'],
                'itbis': calcs['itbis'],
                'total': calcs['total']
            }
        return serverAnswer(True, 'Factura selecionada', bill)
    except:
        return serverAnswer(False, "Error de busqueda")


@app.put('/bills/edit/{b_id}')
def bill_edit(b: BillModel, b_id: int):
    try:
        bill = Bill.get(Bill.bill_id == b_id)
        bill.client_name = b.client_name
        bill.rnc = b.rnc
        bill.b_date = getDate(b.b_date)
        bill.description = b.des
        bill.save()
        return serverAnswer(True, "Factura editada correctamente")
    except:
        return serverAnswer(False, "Error al editar")


@app.put('/detail/edit/{d_id}')
def edit_detail(d: BDetail_Model, d_id: int):
    try:
        det = Bill_Detail.get(Bill_Detail.id_detail == d_id)
        det.id_product = d.id_p
        det.quantity = d.quantity
        for p in Product.select().where(Product.product_id == d.id_p):
            value = p.price * d.quantity
        det.t_value = value
        det.save()
        return serverAnswer(True, "Item de factura editado correctamente")
    except:
        return serverAnswer(False, "Error al editar")


@app.delete('/detail/delete/d_id={d_id}')
def delete_detail(d_id: int):
    try:
        det = Bill_Detail.get(Bill_Detail.id_detail == d_id)
        det.delete_instance()
        return serverAnswer(True, "Detalle eliminado con exito")
    except:
        return serverAnswer(False, "Error en bd")


@app.delete('/bills/delete/b_id={b_id}')
def bill_delete(b_id):
    try:
        bill = Bill.get(Bill.bill_id == b_id)
        query = Bill_Detail.delete().where(Bill_Detail.id_bill == bill.bill_id)
        query.execute()
        bill.delete_instance()
        return serverAnswer(True, "Factura eliminada con exito")
    except:
        return serverAnswer(False, "Error en bd")
