from dataclasses import dataclass
import time
from datetime import datetime
from celery import Celery
import requests
from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource
from flask import send_file
from modelos.modelos import (DefinitionTask, DefinitionTaskSchema, Task,TaskSchema, Usuario, UsuarioSchema, db)
from redis import Redis
from rq import Queue
from pathlib import Path
import smtplib, ssl
import json
#from decouple import config
from urllib.request import urlopen
import random
url = "https://storage.googleapis.com/bucket_music_file_storage_1/enviroments.json?rand_v="+str(random.randint(1,10000000))
response = urlopen(url)
data = json.loads(response.read())

REDIS_URI = data['REDIS_URL']
MAIL_URI = data['MAIL_URL']
print(url,flush=True)
print(REDIS_URI,flush=True)
print(MAIL_URI,flush=True)

UPLOAD_DIRECTORY = "/usr/src/app/upfiles/"
PROCESS_DIRECTORY = "/usr/src/app/pofiles/"

celery_app = Celery('tasks', broker='redis://{}/0'.format(REDIS_URI))


from sqlalchemy.exc import IntegrityError

usuario_schema = UsuarioSchema()
definitionTask_schema = DefinitionTaskSchema()
task_schema = TaskSchema()

@celery_app.task(name="escribir_cola")
def escribir_cola(data):
    pass
    
class statusCheck(Resource):
    def get(self):
        return {'status': 'ok'}

class VistaSignInUser(Resource):
    def post(self):
        print(request)
        if (request.json["password1"] == request.json["password2"]):
            usuario = request.json["username"]
            nuevo_usuario = Usuario(usuario = usuario, 
                                    email = request.json["email"], 
                                    contrasena = request.json["password1"],
                                    phone = '',
                                    rol=1)
            db.session.add(nuevo_usuario)
            db.session.commit()
            token_de_acceso = create_access_token(identity=nuevo_usuario.id)
            return {"mensaje": "usuario creado exitosamente", "token": token_de_acceso, 'usuarioId': nuevo_usuario.id}
        return {"mensaje": "password no coinciden", 'status': 400}

class VistaLogIn(Resource):
    def post(self):
        usuario = Usuario.query.filter(Usuario.usuario == request.json["username"],
                                        Usuario.contrasena == request.json["password"]).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, 'usuarioId': usuario.id}
    
    def put(self):
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                        Usuario.id == request.json["id"],
                                        Usuario.rol == request.json["rol"]).first()
        if(usuario is None):
            return "El usuario no existe", 404
        usuario.contrasena = request.json.get("contrasena_new", usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)
    
    def delete(self):
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                        Usuario.id == request.json["id"],
                                        Usuario.rol == request.json["rol"]).first()
        if(usuario is None):
            return "El usuario no existe", 404
        db.session.delete(usuario)
        db.session.commit()
        return '', 204

class VistaTasks(Resource):
     def get(self):
        try:
            definitionTask = DefinitionTask.query.all()
            if len(definitionTask) > 0 :
                return definitionTask_schema.dump(definitionTask, many=True)
            return {'mensaje': 'No hay actividades que se puedan hacer Programadas', 'status': 403}
        except ConnectionError as e:
            return {'error': 'Backend getTask offline -- Connection'}, 404
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            return {'error': 'Backend getTask offline -- Timeout'}, 404
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            return {'error': 'Backend getTask offline -- ManyRedirects'}, 404
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            return {'error': 'Backend getTask offline -- Request'}, 404
        except Exception as e:
            return {'error': 'Backend getTask - Error desconocido -' + str(e)}, 404

class VistaTask(Resource):
    def post(self, id_task):
        #@jwt_required()
        try:
            file_name = request.json['fileName']
            new_format = request.json['newFormat']

            timestamp = datetime.timestamp(datetime.now())
            status = 'upLoaded'

            usuario = Usuario.query.get_or_404(id_task)
            task = Task(time_stamp = timestamp, 
                        file_name = file_name.split('.')[1],
                        path_file_name = file_name,
                        new_format = new_format,
                        status = status,
                        id_usuario = usuario.id)
            db.session.add(task)
            db.session.commit()
            
            data = {'file_name' : file_name, 
                    'new_format' : new_format, 
                    'id_task': task.id}
            args = (data,)
            print(args)
            escribir_cola.apply_async(args = args)
            return {'status': 'Tarea encolada correctamente', 'id_task': task.id }, 200
        except ConnectionError as e:
            return {'error': 'Backend postTask offline -- Connection'}, 404
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            return {'error': 'Backend postTask offline -- Timeout'}, 404
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            return {'error': 'Backend postTask offline -- ManyRedirects'}, 404
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            return {'error': 'Backend postTask offline -- Request'}, 404
        except Exception as e:
            return {'error': 'Backend postTask - Error desconocido -' + str(e)}, 404 
    
    def get(self, id_task):
        #@jwt_required()
        try:
            task = Task.query.get_or_404(id_task)
            if task is not None:
                return task_schema.dump(task, many=False)
            return 'La tarea no se encontro' , 404 
        except ConnectionError as e:
            return {'error': 'Backend getTask offline -- Connection'}, 404
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            return {'error': 'Backend getTask offline -- Timeout'}, 404
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            return {'error': 'Backend getTask offline -- ManyRedirects'}, 404
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            return {'error': 'Backend getTask offline -- Request'}, 404
        except Exception as e:
            return {'error': 'Backend getTask - Error desconocido -' + str(e)}, 404 
    
    def put(self, id_task):
         #@jwt_required()
        try:
            task = Task.query.get_or_404(id_task)
            if task is not None:
                new_format = request.json['newFormat']
                task.new_format = new_format
                db.session.commit()
                return task_schema.dump(task)     
            return 'La tarea a actualizar no se encontro' , 404
        except ConnectionError as e:
            return {'error': 'Backend putTask offline -- Connection'}, 404
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            return {'error': 'Backend putTask offline -- Timeout'}, 404
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            return {'error': 'Backend putTask offline -- ManyRedirects'}, 404
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            return {'error': 'Backend putTask offline -- Request'}, 404
        except Exception as e:
            return {'error': 'Backend putTask - Error desconocido -' + str(e)}, 404

    def delete(self, id_task):
         #@jwt_required()
        try:
            task = Task.query.get_or_404(id_task)
            if task is not None :
                db.session.delete(task)
                db.session.commit()
                return 'la tarea se elimino correctamente', 200
            return 'la tarea a eliminar no se encontro', 404
        except ConnectionError as e:
            return {'error': 'Backend deleteTask offline -- Connection'}, 404
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            return {'error': 'Backend deleteTask offline -- Timeout'}, 404
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            return {'error': 'Backend deleteTask offline -- ManyRedirects'}, 404
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            return {'error': 'Backend deleteTask offline -- Request'}, 404
        except Exception as e:
            return {'error': 'Backend deleteTask - Error desconocido -' + str(e)}, 404 

class VistaFiles(Resource):
    def get(self, file_name):
        try:
            task = Task.query.filter(Task.path_file_name == file_name,
                                        Task.status ==  "Procesed").first()
            if task is not None:
                return {'path_file_name': PROCESS_DIRECTORY+ task.new_format, 'file_name': task.new_format}
            else:
                return 'El archivo no existe o no ha sido procesado', 404  
            #return {'path_file_name': PROCESS_DIRECTORY +"basto.wav", 'file_name': "basto.wav"}
        except ConnectionError as e:
            return {'error': 'Servicio InfoTemp offline -- Connection'}, 404
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            return {'error': 'Servicio InfoTemp offline -- Timeout'}, 404
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            return {'error': 'Servicio InfoTemp offline -- ManyRedirects'}, 404
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            return {'error': 'Servicio InfoTemp offline -- Request'}, 404
        except Exception as e:
            return {'error': 'Servicio InfoTemp - Error desconocido -' + str(e)}, 404

class VistaActualizar(Resource):
    def put(self, id_task):
        try:
            print(id_task,flush=True)
            task = Task.query.get_or_404(id_task)
            if(task is not None):
                task.status = "Procesed"
                db.session.commit()
                print('Task procesed',flush=True)
                print(task.status,flush=True)
                usuario = Usuario.query.get_or_404(task.id_usuario)
                email = usuario.email
                if (email == ""):
                    return {'status':'El usuario no tiene un correo registrado'}, 404
                
                print(usuario,flush=True)
                self.enviar_correo(email, id_task)
                return {'status': "la tarea actualizacion de la tarea se realizo con exito"}, 200
            else:
                return {'status': "la tarea no se encontro "}, 404
        except Exception as e:
            return {'status': 'Servicio InfoTemp - Error desconocido -' + str(e)}, 404

    def enviar_correo(self, sender_email, id_task):
        url_mail = 'http://{}/api/mail'.format(MAIL_URI)
        data_mail = {'mail' : sender_email,
                    'id_task': str(id_task)}
        print(url_mail)
        send_m = requests.post(url_mail, json=data_mail) 
        if(send_m.status_code == 200):
            print('ok mail sent')
        else:
            print('error sending mail...')
