import email
import re
import datetime
from redis import Redis
from rq import Queue
from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from modelos.modelos import db, Usuario, UsuarioSchema, DefinitionTask, DefinitionTaskSchema

usuario_schema = UsuarioSchema()
definitionTask_schema = DefinitionTaskSchema()


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
        try:
            file_name = request.json['fileName']
            new_format = request.json['newFormat']
            #TODO: faltan campos
            task = requests.post(url_back, json=dataBudy) 
            return task.json(), 200
            q = Queue(connection=Redis())
            q.enqueue('taskId', 990 + i, 
                       'file_name', file_name,
                       'new_format', new_format)

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
        try:
            url_back = 'http://localhost:5000/task/{}'.format(id_task)
            task = requests.post(url_back) 
            return task.json(), 200
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
        try:
            url_back = 'http://localhost:5000/task/{}'.format(id_task)
            dataBudy = {'new_format': request.json['newFormat']}
            task = requests.post(url_back, json=dataBudy) 
            return task.json(), 200
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
        try:
            url_back = 'http://localhost:5000/task/{}'.format(id_task)
            task = requests.post(url_back) 
            return task.json(), 200
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