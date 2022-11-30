from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from modelos.modelos import db
from vistas import VistaLogIn, VistaSignInUser, VistaFiles, VistaTask, statusCheck, VistaTasks, VistaActualizar, VistaTsk
import json
#from decouple import config
from urllib.request import urlopen

import random
url = "https://storage.googleapis.com/bucket_music_file_storage_1/enviroments.json?rand_v="+str(random.randint(1,10000000))
response = urlopen(url)
data = json.loads(response.read())


app = Flask(__name__)
DATABASE_URI = data['DATABASE_URL']

#DATABASE_URI = 'postgresql://postgres:DreamTeam123*@35.224.243.237:5432/postgres'
print(url,flush=True)
print(DATABASE_URI,flush=True)

#DATABASE_URI = config('DATABASE_URL')  

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True
app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()
cors = CORS(app)


api = Api(app)



api.add_resource(statusCheck, '/api/status')
api.add_resource(VistaSignInUser, '/api/auth/signup')
api.add_resource(VistaLogIn, '/api/auth/login')
api.add_resource(VistaTasks, '/api/tasks')
api.add_resource(VistaTask, '/api/task/<int:id_task>')
api.add_resource(VistaTsk, '/api/taskUpdSt/<int:id_task>')
api.add_resource(VistaFiles, '/api/files/<string:file_name>')

api.add_resource(VistaActualizar, '/api/taskUpd/<int:id_task>')

jwt = JWTManager(app)


print(' * BACKEND corriendo ----------------')

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=5000,debug=True)
    HOST = '0.0.0.0'
    PORT = 8080
    app.run(HOST, PORT, debug=True) 
