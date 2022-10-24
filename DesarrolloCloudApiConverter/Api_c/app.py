#from Api import create_app
from markupsafe import escape
from flask_restful import Api
from vistas.vistas import VistaSingUp, VistaLogIn, VistaTask, VistaFiles, statusCheck, VistaTasks 

from flask import Flask
from flask_cors import CORS
import os

UPLOAD_DIRECTORY = "/usr/src/app/upfiles"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

def create_app(config_name):
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_DIRECTORY
    CORS(app)
    return app

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)

api.add_resource(statusCheck, '/api/status')
api.add_resource(VistaSingUp, '/api/auth/signup')
api.add_resource(VistaLogIn, '/api/auth/login')
api.add_resource(VistaTasks, '/api/tasks')
api.add_resource(VistaTask, '/api/task/<int:id_task>')
api.add_resource(VistaFiles, '/api/files/<string:file_name>')

print(' * API corriendo ----------------')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001,debug=True)