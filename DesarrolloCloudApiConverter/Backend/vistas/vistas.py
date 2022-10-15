import email
import re
from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from modelos.modelos import db, Usuario, UsuarioSchema
usuario_schema = UsuarioSchema()




class VistaSignInUser(Resource):
    
    def post(self):
        nuevo_usuario = Usuario(usuario=request.json["usuario"], 
                                email=request.json["u_email"], 
                                contrasena=request.json["contrasena"], 
                                phone = request.json["phone"],
                                rol=1, 
                                no_cuenta='', 
                                nombre_banco='', 
                                saldo=0.0, 
                                medio_pago='')
        db.session.add(nuevo_usuario)
        db.session.commit()
        token_de_acceso = create_access_token(identity=nuevo_usuario.id)
        return {"mensaje": "usuario apostador creado exitosamente", "token": token_de_acceso, "id": nuevo_usuario.id, "rol": nuevo_usuario.rol}

class VistaLogIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                        Usuario.contrasena == request.json["contrasena"]).first()
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
        ##usuario = Usuario.query.get_or_404(id_usuario)
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                        Usuario.id == request.json["id"],
                                        Usuario.rol == request.json["rol"]).first()
        if(usuario is None):
            return "El usuario no existe", 404
        db.session.delete(usuario)
        db.session.commit()
        return '', 204

