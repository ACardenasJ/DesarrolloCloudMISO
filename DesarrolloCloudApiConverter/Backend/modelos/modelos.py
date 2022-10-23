from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from decimal import Decimal as D 
import sqlalchemy.types as types  

class SqliteNumeric(types.TypeDecorator):     
    impl = types.String     
    def load_dialect_impl(self, dialect):         
        return dialect.type_descriptor(types.VARCHAR(100))     
    def process_bind_param(self, value, dialect):         
        return str(value)     
    def process_result_value(self, value, dialect):         
        return D(value)  


db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    email = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    rol = db.Column(db.Integer, default=True)
    phone = db.Column(db.String(50))
    

class DefinitionTask(db.Model):
    __tablename__ = 'definitionTask'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    origen = db.Column(db.String(50))
    destino = db.Column(db.String(50))

class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    time_stamp = db.Column(db.String(50))
    file_name = db.Column(db.String(50))
    path_file_name = db.Column(db.String(50))
    new_format = db.Column(db.String(50))
    status = db.Column(db.String(50))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True

class DefinitionTaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DefinitionTask
        include_relationships = True
        load_instance = True

class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_relationships = True
        load_instance = True