import email
import re
import time
import uuid
from datetime import datetime

from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource
from flask import send_file
from modelos.modelos import (DefinitionTask, DefinitionTaskSchema, Task,
                             TaskSchema, Usuario, UsuarioSchema, db)
from redis import Redis
from rq import Queue

from sqlalchemy.exc import IntegrityError

usuario_schema = UsuarioSchema()
definitionTask_schema = DefinitionTaskSchema()
task_schema = TaskSchema()

class VistaSignInUser(Resource):
    def post(self):
        if request.json["password1"] == request.json["password2"]:
                nuevo_usuario = Usuario(usuario=request.json["usuario"], 
                                        email=request.json["email"], 
                                        contrasena=request.json["password1"],
                                        phone = '',
                                        rol=1)
                db.session.add(nuevo_usuario)
                db.session.commit()
                token_de_acceso = create_access_token(identity=nuevo_usuario.id)
                return {"mensaje": "usuario apostador creado exitosamente", "token": token_de_acceso, "id": nuevo_usuario.id, "rol": nuevo_usuario.rol}
        return {"mensaje": "password no coinciden", 'status': 400}

class VistaLogIn(Resource):
    def post(self):
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                        Usuario.contrasena == request.json["password"]).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "rol": usuario.rol}
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


class VistaTask(Resource):
    def get(self):
        try:
           definitionTask = DefinitionTask.query.all()
           if len(definitionTask) > 0 :
                return definitionTask_schema.dump(definitionTask, many=True)
           return {'mensaje': 'No hay tareas programdas', 'status': 404}
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

    def post(self):
        #@jwt_required()
        # TODO: tengo que ver como desencolar en otro programa y ver como enviar archivos
        try:
            file_name = request.json['fileName']
            new_format = request.json['newFormat']
            uuid= uuid.uuid4()
            now = datetime.now()
            timestamp = datetime.timestamp(now)
            status = 'uploaded'
            taskId = uuid

            task = Task(taskId=taskId, 
                        time_stamp = timestamp, 
                        file_name = file_name,
                        path_file_name = '',
                        new_format = new_format,
                        path_new_format = '',
                        status = status)
            db.session.add(task)
            db.session.commit()

            q = Queue(connection=Redis())
            job = q.enqueue('taskId:', taskId, 
                      'time_stamp:', timestamp,
                      'file_name:', file_name,
                      'new_format:', new_format,
                      'status:', status)
            time.sleep(2)
            if(job is not None):
                 return {'mensaje': 'Se encolo correctmente', 'status': 200}
            return {'mensaje': 'No se encolo la tarea', 'status': 409}
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
    
    def get(self, id_task):
        #@jwt_required()
        try:
            task = Task.query.get_or_404(id_task)
            if task is not None:
                return task_schema.dump(eventosDeportivos, many=True)
            return 'La tarea no se encontro' , 404 
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

    def delete(self, id_task):
         #@jwt_required()
        try:
            task = Task.query.get_or_404(id_task)
            db.session.delete(eventod)
            db.session.commit()
            return 'la tarea se elimino correctamente', 204
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

class VistaFiles(Resource):
    def get(self, file_name):
        try:
            extension = file_name.split(".")
            task = Task.query.filter(Task.file_name == file_name).all()
            if task.file_name == file_name:
                return send_file(
                    task.path_file_name,
                    mimetype="audio/" +extension[1], 
                    as_attachment=True, 
                    attachment_filename=task.file_name)
            elif (task.new_format == file_name) and (task.status == 'procesed'):
                 return send_file(
                    task.path_new_format,
                    mimetype= 'audio/' + extension[1], 
                    as_attachment=True, 
                    attachment_filename=task.path_new_format)
            else:
                 return 'El archivo no existe o no ha sido procesado', 204  
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

