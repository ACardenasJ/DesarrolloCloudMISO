from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from modelos.modelos import db
from vistas import VistaLogIn, VistaSignInUser



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nube.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True
app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()
cors = CORS(app)


api = Api(app)




api.add_resource(VistaSignInUser, '/api/auth/signup')
api.add_resource(VistaLogIn, '/login')
#api.add_resource(VistaTask, '/api/task/<int:id_task>')
#api.add_resource(VistaFiles, '/api/files/<string:file_name>')

jwt = JWTManager(app)

