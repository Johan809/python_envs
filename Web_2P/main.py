from fastapi import FastAPI
from pydantic import BaseModel
from peewee import *
from data import *

app = FastAPI()
sesions = []
db.connect()
db.create_tables([User, Secret], safe=True)


class UserModel(BaseModel):
    name: str
    email: str
    password: str


class SecretModel(BaseModel):
    title: str
    des: str
    money: float
    s_date: str
    place: str
    lat: float
    lng: float


@app.get('/')
def index():
    users = []
    secrets = []
    for u in User.select():
        user = {
            'name': u.name,
            'email': u.email,
            'password': u.password
        }
        users.append(user)
    for s in Secret.select():
        secret = {
            'id': s.s_id,
            'owner': s.owner.name,
            'title': s.title,
            'des': s.description,
            'money': s.money,
            'date': s.s_date,
            'place': s.place,
            'lat': s.lat,
            'lng': s.lng
        }
        secrets.append(secret)
    return {'users': users, 'secrets': secrets, 'sesions': sesions}


@app.post('/regUser')
def create_user(user: UserModel):
    for u in User.select():
        if user.name == u.name and user.email == u.email:
            return {'ok': False, 'msg': 'El usuario ya existe'}
    newUser = User(name=user.name, email=user.email, password=user.password)
    newUser.save()
    return {'ok': True, 'msg': 'El Usuario ha sido registrado con exito'}


@app.get('/login/email={email}&password={password}')
def user_login(email: str, password: str):
    query = User.select().where((User.email == email) & (User.password == password))
    for u in query:
        token = generate_token()
        sesion = {
            'email': u.email,
            'token': token
        }
        sesions.append(sesion)
        msg = f"La sesion de {u.email} ha sido iniciada con exito"
        return {'ok': True, 'msg': msg, 'token': token}
    return {'ok': False, 'msg': 'Credenciales Invalidas'}


@app.get('/modify/{token}/newName={newName}&newEmail={newEmail}')
def user_modify(token: str, newName: str, newEmail: str):
    for ses in sesions:
        if token == ses['token']:
            selected_email = ses['email']
            ses['email'] = newEmail
            actual_user = User.select().where(User.email == selected_email).get()
            actual_user.name = newName
            actual_user.email = newEmail
            actual_user.save()
            return{'ok': True, 'msg': 'Los datos han sido actualizados con exito'}
    return {'ok': False, 'msg': 'Token invalido'}


@app.get('/change/{token}/oldpass={oldpass}&newpass={newpass}')
def user_change(token: str, oldpass: str, newpass: str):
    for ses in sesions:
        if token == ses['token']:
            try:
                actual_user = User.get(
                    (User.email == ses['email']) & (User.password == oldpass))
                actual_user.password = newpass
                actual_user.save()
                return{'ok': True, 'msg': 'Los datos han sido actualizados con exito'}
            except:
                return {'ok': False, 'msg': 'Contraseña erronea'}
    return {'ok': False, 'msg': 'Token invalido'}

@app.post('/secret-post/{token}')
def create_secret(secret:SecretModel, token:str):
    for ses in sesions:
        if token == ses['token']:
            actual_user = User.get(User.email == ses['email'])
            sDate = getDate(secret.s_date)
            newSecret = Secret( owner = actual_user, title = secret.title, description = secret.des,
            money = secret.money, s_date= sDate, place = secret.place, 
            lat = secret.lat, lng = secret.lng )
            newSecret.save()
            msg = f"El nuevo secreto de {actual_user.name} ha sido guardado con exito"
            return{'ok': True, 'msg': msg}
    return {'ok': False, 'msg': 'Token invalido'}

@app.get('/secret-get/{token}')
def get_secrets(token:str):
    secrets = []
    for ses in sesions:
        if token == ses['token']:
            try:
                actual_user = User.get(User.email == ses['email'])
                for s in Secret.select().join(User).where( User.name == actual_user.name ):
                    secret = {
                        'id': s.s_id,
                        'owner': s.owner.name,
                        'title': s.title,
                        'des': s.description,
                        'money': s.money,
                        'date': s.s_date,
                        'place': s.place,
                        'lat': s.lat,
                        'lng': s.lng
                    }
                    secrets.append(secret)
                    return {'ok': True, 'secrets': secrets}    
            except:
                return {'ok': False, 'msg': 'Error de busqueda'}
    return {'ok': False, 'msg': 'Token invalido'}

@app.delete('/secret-del/{token}/secret_id={s_id}')
def del_secret(token:str, s_id:int):
    for ses in sesions:
        if token == ses['token']:
            try:
                actual_user = User.get(User.email == ses['email'])
                selected_s = Secret.select().join(User).where((User.name == actual_user.name) & (Secret.s_id == s_id)).get()
                selected_s.delete_instance()
                msg = f"El secreto de {actual_user.name} con id {s_id} ha sido eliminado con exito"
                return {'ok': True, 'msg': msg}    
            except:
                return {'ok': False, 'msg': 'Error de busqueda'}
    return {'ok': False, 'msg': 'Token invalido'}

@app.delete('/logout/{token}')
def user_logout(token: str):
    count = 0
    for ses in sesions:
        if token == ses['token']:
            sesions.pop(count)
            msg = f"La sesion de {ses['email']} ha sido cerrada correctamente"
            return{'ok': True, 'msg': msg}
        count += 1
    return {'ok': False, 'msg': 'Token invalido'}


db.close()
