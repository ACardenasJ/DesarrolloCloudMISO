from lib2to3.pytree import convert
from markupsafe import escape
from flask_restful import Api
from vistas.convertidor import converter as convertidor_
from vistas import statusCheck, doTask
from flask import Flask
from flask_cors import CORS
import os

PROCESS_DIRECTORY = "/usr/src/app/pofiles"
file_path_redis = "./vistas/programar_task.txt"

if not os.path.exists(PROCESS_DIRECTORY):
    os.makedirs(PROCESS_DIRECTORY)

def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    return app

app = create_app('default')
app_context = app.app_context()
app_context.push()
api = Api(app)

api.add_resource(statusCheck, '/api/status')
api.add_resource(doTask, '/api/convertidor')

print(' * CONVERTER corriendo ----------------')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002,debug=True)
