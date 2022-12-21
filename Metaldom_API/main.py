import os
import shutil
import uvicorn
import data as d
from peewee import *
from typing import List
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from models import userModel, requestModel, evaluationModel, c_resumeModel

path = os.getcwd()
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
tables = [d.User, d.Request, d.Request_Answer,
          d.Evaluation, d.Files, d.C_Resume]
d.db.connect()
d.db.create_tables(tables, safe=True)


@app.get('/')
def index():
    return d.serverAnswer(True, 'Conectado')


@app.post('/regUser')
def create_User(user: userModel):
    try:
        newUser = d.User(username=user.username, name=user.name,
                         email=user.email, pwd=user.pwd, is_dev=user.is_dev)
        newUser.save()
        return d.serverAnswer(True, 'User registrado', newUser)
    except:
        return d.serverAnswer(False, 'Error')


@app.get('/getUsers')
def get_users():
    try:
        all_users = []
        for u in d.User.select():
            one_user = {
                'id': u._id,
                'username': u.username,
                'name': u.name,
                'email': u.email,
                'dev?': u.is_dev
            }
            all_users.append(one_user)
        return d.serverAnswer(True, 'Todos los users', all_users)
    except:
        return d.serverAnswer(False, 'Error')


@app.get('/getUser/{_id}')
def get_user(_id: int):
    try:
        u = d.User.select().where(d.User._id == _id).get()
        one_user = {
            'id': u._id,
            'username': u.username,
            'name': u.name,
            'email': u.email,
            'dev?': u.is_dev
        }
        return d.serverAnswer(True, 'Usuario elegido', one_user)
    except:
        return d.serverAnswer(False, 'Error')


@app.get('/getReq/{_id}')
def get_Req(_id: int):
    try:
        r = d.Request.select().where(d.Request._id == _id).get()
        one_request = {
            'id': r._id,
            'client': r.id_client,
            'request_type': r.request_type,
            'description': r.description,
            'creation_date': r.creation_date,
            'was_attended': r.was_attended
        }
        return d.serverAnswer(True, 'Solicitud elegido', one_request)
    except:
        return d.serverAnswer(False, 'Error')


@app.get('/getReqs')
def get_Reqs():
    try:
        all_req = []
        for r in d.Request.select():
            one_req = {
                'id': r._id,
                'client': r.id_client,
                'request_type': r.request_type,
                'description': r.description,
                'creation_date': r.creation_date,
                'was_attended': r.was_attended
            }
            all_req.append(one_req)
        return d.serverAnswer(True, 'Todas las solicitudes', all_req)
    except:
        return d.serverAnswer(False, 'Error')


@app.post('/regReq')
def create_Req(req: requestModel):
    try:
        _date = d.getDate(req.creation_date)
        newReq = d.Request(id_client=req.client, request_type=req.req_type,
                           description=req.description, creation_date=_date, was_attended=req.was_attended)
        newReq.save()
        return d.serverAnswer(True, 'La Solicitud ha sido guardada', newReq)
    except:
        return d.serverAnswer(False, 'Error')


@app.post('/regReqAns')
def create_Req_Ans():
    try:
        newReqAns1 = d.Request_Answer(
            id_request=1, id_dev=1, meet_link='https://www.unlink.com', comment="Comentario 1")
        newReqAns2 = d.Request_Answer(
            id_request=2, id_dev=2, meet_link='https://www.unlink.com', comment='Comentario 2')
        newReqAns3 = d.Request_Answer(
            id_request=3, id_dev=2, meet_link='https://www.unlink.com', comment='Comentario 3')
        newReqAns1.save()
        newReqAns2.save()
        newReqAns3.save()
        return d.serverAnswer(True, 'Respuestas Creadas', [newReqAns1, newReqAns2, newReqAns3])
    except:
        return d.serverAnswer(False, 'Error')


@app.get('/getAns')
def get_all_Ans():
    try:
        all_ans = []
        for a in d.Request_Answer.select():
            one_ans = {
                'id': a._id,
                'request': a.id_request,
                'dev': a.id_dev,
                'meet_link': a.meet_link,
                'comment': a.comment
            }
            all_ans.append(one_ans)
        return d.serverAnswer(True, 'Todas las respuestas', all_ans)
    except:
        return d.serverAnswer(False, 'Error')


@app.get('/getAns/{_id}')
def get_one_Ans(_id: int):
    try:
        a = d.Request_Answer.select().where(d.Request_Answer._id == _id).get()
        one_ans = {
            'id': a._id,
            'request': a.id_request,
            'dev': a.id_dev,
            'meet_link': a.meet_link,
            'comment': a.comment
        }
        return d.serverAnswer(True, 'Respuesta elegida', one_ans)
    except:
        return d.serverAnswer(False, 'Error')


@app.post('/reqEva')
def create_Evaluation(eva: evaluationModel):
    try:
        newEva = d.Evaluation(
            id_request=eva.request, id_answer=eva.answer, investment_return=eva.investment_return, description=eva.description)
        newEva.save()
        return d.serverAnswer(True, 'Evaluacion guardada', newEva)
    except (RuntimeError, TypeError, NameError) as err:
        print(err)
        return d.serverAnswer(False, 'Error')


@app.get('/getEvas')
def get_Evas():
    try:
        all_evas = []
        for e in d.Evaluation.select():
            one_eva = {
                'id': e._id,
                'request': e.id_request,
                'answer': e.id_answer,
                'cotization': d.getTotal(e._id),
                'cotization_resume': d.getResume(e._id),
                'investment_return': e.investment_return
            }
            all_evas.append(one_eva)
        return d.serverAnswer(True, 'Todas las evaluaciones', all_evas)
    except:
        return d.serverAnswer(False, 'Error')


@app.get('/getEva/{_id}')
def get_Eva(_id: int):
    try:
        e = d.Evaluation.select().where(d.Evaluation._id == _id).get()
        one_eva = {
            'id': e._id,
            'request': e.id_request,
            'answer': e.id_answer,
            'cotization': d.getTotal(e._id),
            'cotization_resume': d.getResume(e._id),
            'files': d.getFiles(e._id),
            'investment_return': e.investment_return
        }
        return d.serverAnswer(True, 'Evaluacion elegida', one_eva)
    except (RuntimeError, TypeError, NameError) as err:
        print(err)
        return d.serverAnswer(False, 'Error')


@app.post('/regResume')
def create_resume(re: c_resumeModel):
    try:
        newResume = d.C_Resume(
            id_eva=d.getLastEvaID(), description=re.description, value=re.value)
        newResume.save()
        return d.serverAnswer(True, 'Resume guardado', newResume)
    except (RuntimeError, TypeError, NameError) as err:
        print(err)
        return d.serverAnswer(False, 'Error')


@app.post('/files')
async def up_files(file: List[UploadFile] = File(...)):
    try:
        for f in file:
            newFile = d.Files(id_eva=d.getLastEvaID(),
                              uri=f'/files/{f.filename}')
            newFile.save()
            with open(f'./files/{f.filename}', 'wb') as buffer:
                shutil.copyfileobj(f.file, buffer)
        return d.serverAnswer(True, 'Archivos guardados')
    except (RuntimeError, TypeError, NameError) as err:
        print(err)
        return d.serverAnswer(False, 'Error')


@app.get('/get_files')
async def get_files():
    try:
        all_files = []
        for f in d.Files.select():
            one_file = {
                'id': f._id,
                'eva': f.id_eva,
                'uri': f.uri
            }
            all_files.append(one_file)
        return d.serverAnswer(True, 'Todos los archivos', all_files)
    except:
        return d.serverAnswer(False, 'Error')


@app.get('/down_files/{_id}')
async def down_files(_id: int):
    try:
        all_files = []
        for f in d.Files.select().join(d.Evaluation).where(d.Evaluation._id == _id):
            file_path = path + f.uri
            all_files.append(file_path)
        return d.zipfiles(all_files)
    except:
        return d.serverAnswer(False, 'Error')


d.db.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
