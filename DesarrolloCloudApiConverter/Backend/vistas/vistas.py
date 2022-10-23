from dataclasses import dataclass
import time
from datetime import datetime
from celery import Celery
import requests
from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource
from flask import send_file
from modelos.modelos import (DefinitionTask, DefinitionTaskSchema, Task,
                             TaskSchema, Usuario, UsuarioSchema, db)
from redis import Redis
from rq import Queue

celery_app = Celery('tasks', broker='redis://localhost:6379/0')


from sqlalchemy.exc import IntegrityError

usuario_schema = UsuarioSchema()
definitionTask_schema = DefinitionTaskSchema()
task_schema = TaskSchema()

@celery_app.task(name="escribir_cola")
def escribir_cola(self, data):
        data = (data,)
        with open('programar_task.txt','a+') as file:
                   file.write('{}\n'.format(data))

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
            return {"mensaje": "usuario apostador creado exitosamente", "token": token_de_acceso}
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
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}
    
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
           return {'mensaje': 'No hay actividades que se puedan ahcer Programadas', 'status': 403}
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
        # TODO: tengo que ver como desencolar en otro programa y ver como enviar archivos
        try:
            file_name = request.json['fileName']
            new_format = request.json['newFormat']
            #id_user = request.json['idUser']
            print("file_name ", file_name)
            timestamp = datetime.timestamp(datetime.now())
            status = 'upLoaded'

            usuario = Usuario.query.get_or_404(id_task)
            
            data = {'file_name' : file_name, 
                    'new_format' : new_format, 
                    'timestamp' : timestamp,
                    'status' : status, 
                    'id_usuario': usuario.id,
                    'email': usuario.email}

            str_data = 'file_name:' + file_name + ",".format('new_format:' + new_format + ',',
                        'timestamp:' +  str(timestamp)  +',',
                        'status:' + status   +',', 
                        'id_usuario:' +  str(usuario.id)  +',', 
                        'email:' + usuario.email)

            task = Task(time_stamp = timestamp, 
                        file_name = file_name.split('.')[1],
                        path_file_name = file_name,
                        new_format = new_format,
                        status = status,
                        id_usuario = usuario.id)
            db.session.add(task)
            db.session.commit()

            #escribir_cola.apply_async(args = str_data)

            q = Queue(connection=Redis())
            job = q.enqueue(str_data)
            time.sleep(1)
            if(job is not None):
                 return {'mensaje': 'Se encolo correctmente', 'status': 200}
            return {'mensaje': 'No se encolo la tarea', 'status': 409}
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
            print('file_name', file_name)
            task = Task.query.filter(Task.file_name == file_name,
                                     Task.status ==  "Procesed").first()

            """  return send_file(
                    task.path_file_name,
                    attachment_filename=task.file_name,
                    as_attachment=True) """
            if task is not None:
                return {'path_file_name': task.path_file_name, 'file_name': task.file_name}
            else:
                 return 'El archivo no existe o no ha sido procesado', 404  
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