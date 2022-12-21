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
    "http://localhost:8100",
    "http://127.0.0.1:8000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
sesions = []
db.connect()
db.create_tables([User, Secret], safe=True)


class UserModel(BaseModel):
    name: str
    email: str
    password: str


class SecretModel(BaseModel):
    title: str
    description: str
    money: int
    date_secret: str
    place: str
    lat: float
    lng: float


@app.get('/')
def index():
    users = []
    secrets = []
    for u in User.select():
        user = {
            'Name': u.name,
            'Email': u.email,
            'Pass': u.password
        }
        users.append(user)
    for s in Secret.select():
        secret = {
            'S_id': s.s_id,
            'Owner': s.owner.name,
            'Title': s.title,
            'Des': s.description,
            'Money': s.money,
            'Date': s.date_secret,
            'Place': s.place,
            'Lat': s.lat,
            'Lng': s.lng
        }
        secrets.append(secret)
    return {'Users': users, 'Secrets': secrets, 'Sesions': sesions}


@app.get('/{token}')
def actual_user(token: str):
    for ses in sesions:
        if token == ses['token']:
            u = User.select().where(User.email == ses['email']).get()
            user = {
                'Name': u.name,
                'Email': u.email,
                'Pass': u.password
            }
            return {'ok': True, 'user': user}
    return {'ok': False, 'Razon': 'Token invalido'}


@app.post('/regUser')
def create_user(user: UserModel):
    for u in User.select():
        if user.name == u.name and user.email == u.email:
            return {'ok': False, 'Razon': 'El usuario ya existe'}

    newUser = User(
        name=user.name, email=user.email, password=user.password)
    newUser.save()
    return {'ok': True, 'Razon': 'El usuario ha sido creado correctamente'}


@app.get('/login/email={email}&password={password}')
def user_login(email: str, password: str):
    query = User.select().where((User.email == email) & (User.password == password))
    for u in query:
        token = generate_token()
        sesion = {
            'token': token,
            'email': u.email
        }
        sesions.append(sesion)
        msg = f"Sesion de {sesion['email']} iniciada correctamente"
        return {'ok': True, 'Razon': msg, 'Token': token}
    return {'ok': False, 'Razon': 'Credenciales invalidas'}


@app.get('/modify/{token}/newName={newName}&newEmail={newEmail}')
def modify_user(token: str, newName: str, newEmail: str):
    for ses in sesions:
        if token == ses['token']:
            selected_email = ses['email']
            ses['email'] = newEmail
            actual_user = User.select().where(User.email == selected_email).get()
            actual_user.name = newName
            actual_user.email = newEmail
            actual_user.save()
            return {'ok': True, 'Razon': 'Los datos han sido actualizados correctamente'}
    return {'ok': False, 'Razon': 'Token invalido'}


@app.get('/change/{token}/oldpass={oldpass}&newpass={newpass}')
def change_password(token: str, oldpass: str, newpass: str):
    for ses in sesions:
        if token == ses['token']:
            try:
                actual_user = User.get(User.password == oldpass)
            except:
                return {'ok': False, 'Razon': 'Contraseña erronea'}
            if actual_user.email == ses['email']:
                actual_user.password = newpass
                actual_user.save()
                return {'ok': True, 'Razon': 'Los datos han sido actualizados correctamente'}
    return {'ok': False, 'Razon': 'Token invalido'}


@app.post('/secret-post/{token}')
def create_secret(secret: SecretModel, token: str):
    for ses in sesions:
        if token == ses['token']:
            actual_user = User.get(User.email == ses['email'])
            sDate = getDate(secret.date_secret)
            newSecret = Secret(owner=actual_user, title=secret.title, description=secret.description,
                               money=secret.money, date_secret=sDate, place=secret.place,
                               lat=secret.lat, lng=secret.lng)
            newSecret.save()
            msg = f"El nuevo secreto de {actual_user.name} ha sido guardado correctamente"
            return {'ok': True, 'Razon': msg}
    return {'ok': False, 'Razon': 'Token invalido'}


@app.get('/secret-get/{token}')
def get_secrets(token: str):
    secrets = []
    for ses in sesions:
        if token == ses['token']:
            try:
                actual_user = User.get(User.email == ses['email'])
                for s in Secret.select().join(User).where(User.name == actual_user.name):
                    secret = {
                        'ID': s.s_id,
                        'Dueño': s.owner.name,
                        'Titulo': s.title,
                        'Descripcion': s.description,
                        'Dinero': s.money,
                        'Fecha': s.date_secret,
                        'Lugar': s.place,
                        'Latitud': s.lat,
                        'Longitud': s.lng
                    }
                    secrets.append(secret)
                return {'ok': True, 'Tus Secretos': secrets}
            except:
                return {'ok': False, 'Razon': 'Error de busqueda'}
    return {'ok': False, 'Razon': 'Token invalido'}


@app.delete('/secret-del/{token}/secret_id={s_id}')
def delete_secret(token: str, s_id: int):
    for ses in sesions:
        if token == ses['token']:
            try:
                actual_user = User.get(User.email == ses['email'])
                selected_sec = Secret.select().join(User).where(
                    (User.name == actual_user.name) & (Secret.s_id == s_id)).get()
                selected_sec.delete_instance()
                msg = f"El secreto con ID {s_id} de {actual_user.name} ha sido eliminado correctamente"
                return {'ok': True, 'Razon': msg}
            except:
                return {'ok': False, 'Razon': 'Error de busqueda, secreto no encontrado'}
    return {'ok': False, 'Razon': 'Token invalido'}


@app.delete('/logout/{token}')
def user_logout(token: str):
    count = 0
    for ses in sesions:
        if token == ses['token']:
            sesions.pop(count)
            msg = f"La sesion de {ses['email']} ha sido cerrada correctamente"
            return {'ok': True, 'Razon': msg}
        count += 1
    return {'ok': False, 'Razon': 'Token invalido'}


db.close()
