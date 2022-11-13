from lib2to3.pytree import convert
from markupsafe import escape
from flask_restful import Api
from flask import Flask
from flask_cors import CORS
from vistas import statusCheck, ManageBucket
from decouple import config
from os import environ


def create_app(config_name):
    app = Flask(__name__)
    app.config['GOOGLE_APPLICATION_CREDENTIALS'] = './vistas/misonube2022equipo23-8093e2406c0a.json'

    #app.config['GOOGLE_APPLICATION_CREDENTIALS'] = environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    #print(environ.get('GOOGLE_APPLICATION_CREDENTIALS'))
    CORS(app)
    return app

app = create_app('default')

app_context = app.app_context()
app_context.push()
api = Api(app)

api.add_resource(statusCheck, '/api/status')
api.add_resource(ManageBucket, '/api/Bucket/<string:file_name>')




print(' * Up/Down Bucket corriendo ----------------')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005,debug=True)