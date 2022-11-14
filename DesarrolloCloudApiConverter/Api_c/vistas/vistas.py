from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token
import requests
from flask import send_file
#from werkzeug.utils import secure_filename
import os
import json

#from decouple import config
from urllib.request import urlopen
#BACKEND_URL = config('BACKEND_URL')  
#UPLOAD_DIRECTORY = "/usr/src/app/upfiles"
import random
url = "https://storage.googleapis.com/bucket_music_file_storage_1/enviroments.json?rand_v="+str(random.randint(1,10000000))
response = urlopen(url)
data = json.loads(response.read())
BACKEND_URL = data['BACKEND_URL']
BUCKET_URL = data['BUCKET_URL']
print(url,flush=True)
print(BACKEND_URL,flush=True)
print(BUCKET_URL,flush=True)

UPLOAD_DIRECTORY = "./vistas/upfiles/"
PROCESS_DIRECTORY = "./vistas/pofiles/"


class statusCheck(Resource):
    def get(self):
        return {'status': 'ok'}

class VistaSingUp(Resource):
    def post(self):
        #@jwt_required()
        try:
            url_back = 'http://{}/api/auth/signup'.format(BACKEND_URL)
            dataBudy = {'username' : request.json["username"],
                        'password1': request.json['password1'],
                        'password2': request.json['password2'],
                        'email': request.json["email"]}

            register = requests.post(url_back, json=dataBudy)  
            return register.json(), 200
        except ConnectionError as e:
            return {'error': 'Api_c SinguP offline -- Connection'}, 404
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            return {'error': 'Api_c SinguP offline -- Timeout'}, 404
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            return {'error': 'Api_c SinguP offline -- ManyRedirects'}, 404
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            return {'error': 'Api_c SinguP offline -- Request'}, 404
        except Exception as e:
            return {'error': 'Api_c SinguP - Error desconocido -' + str(e)}, 404

class VistaLogIn(Resource):
    def post(self):
        try:
            url_back = 'http://{}/api/auth/login'.format(BACKEND_URL)
            dataBudy = {'username' : request.json['username'],
                        'password': request.json['password']}
            print(url_back)
            logIn = requests.post(url_back, json=dataBudy)  
            return logIn.json(), 200
        except ConnectionError as e:
            return {'error': 'Api_c Login offline -- Connection'}, 404
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            return {'error': 'Api_c Login offline -- Timeout'}, 404
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            return {'error': 'Api_c Login offline -- ManyRedirects'}, 404
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            return {'error': 'Api_c Login offline -- Request'}, 404
        except Exception as e:
            return {'error': 'Api_c Login - Error desconocido -' + str(e)}, 404

class VistaTasks(Resource):
    def get(self):
        try:
            url_back = 'http://{}/api/tasks'.format(BACKEND_URL)
            task = requests.get(url_back) 
            return task.json(), 200
        except ConnectionError as e:
            return {'error': 'Api_c getTask offline -- Connection'}, 404
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            return {'error': 'Api_c getTask offline -- Timeout'}, 404
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            return {'error': 'Api_c getTask offline -- ManyRedirects'}, 404
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            return {'error': 'Api_c getTask offline -- Request'}, 404
        except Exception as e:
            return {'error': 'Api_c getTask - Error desconocido -' + str(e)}, 404
    
class VistaTask(Resource):
    def post(self, id_task):
        try:
            rqt = json.loads(request.form['request_'])
            url_back = 'http://{}/api/task/{}'.format(BACKEND_URL,id_task)
            dataBudy = {'fileName' : rqt['fileName'],
                        'newFormat': rqt['newFormat']}
                        #'id_user' : request.json['idUser']}
            file = request.files['file']
            file_name = file.filename
            filename = os.path.join(UPLOAD_DIRECTORY, file_name)
            file.save(filename)

            url_bucket = 'http://{}/api/BucketUp/{}'.format(BUCKET_URL,file_name)
            file = {'file': open(filename, 'rb')}
            bucket = requests.post(url_bucket, files=file)
            print(bucket.json())
            #GUARDAR ARCHIVO
            print(filename)
            print(dataBudy)
            task = requests.post(url_back, json=dataBudy)
            return task.json(), 200

            #return {'status': 'ok'}, 200
        except ConnectionError as e:
            return {'error': 'Apic_c task post offline -- Connection'}, 404
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            return {'error': 'Apic_c task post offline -- Timeout'}, 404
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            return {'error': 'Apic_c task post offline -- ManyRedirects'}, 404
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            return {'error': 'Apic_c task post offline -- Request'}, 404
        except Exception as e:
            return {'error': 'Apic_c task post - Error desconocido -' + str(e)}, 404
    
    def get(self, id_task):
        try:
            url_back = 'http://{}/api/task/{}'.format(BACKEND_URL, id_task)
            task = requests.get(url_back) 
            return task.json(), 200
        except ConnectionError as e:
            return {'error': 'Api_c getTask offline -- Connection'}, 404
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            return {'error': 'Api_c getTask offline -- Timeout'}, 404
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            return {'error': 'Api_c getTask offline -- ManyRedirects'}, 404
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            return {'error': 'Api_c getTask offline -- Request'}, 404
        except Exception as e:
            return {'error': 'Api_c getTask - Error desconocido -' + str(e)}, 404
    
    def put(self, id_task):
        try:
            url_back = 'http://{}/api/task/{}'.format(BACKEND_URL, id_task)
            dataBudy = {'newFormat': request.json['newFormat']}
            task = requests.put(url_back, json=dataBudy) 
            return task.json(), 200
        except ConnectionError as e:
            return {'error': 'Apic_c putTask offline -- Connection'}, 404
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            return {'error': 'Apic_c putTask offline -- Timeout'}, 404
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            return {'error': 'Apic_c putTask offline -- ManyRedirects'}, 404
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            return {'error': 'Apic_c putTask offline -- Request'}, 404
        except Exception as e:
            return {'error': 'Apic_c putTask - Error desconocido -' + str(e)}, 404

    def delete(self, id_task):
        try:
            url_back = 'http://{}/api/task/{}'.format(BACKEND_URL,id_task)
            task = requests.delete(url_back) 
            return task.json(), 200
        except ConnectionError as e:
            return {'error': 'Apic_c deleteTask offline -- Connection'}, 404
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            return {'error': 'Apic_c deleteTask offline -- Timeout'}, 404
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            return {'error': 'Apic_c deleteTask offline -- ManyRedirects'}, 404
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            return {'error': 'Apic_c deleteTask offline -- Request'}, 404
        except Exception as e:
            return {'error': 'Apic_c deleteTask - Error desconocido -' + str(e)}, 404

class VistaFiles(Resource):
    def get(self, file_name, nfile_name):
        try:
            url_back = 'http://{}/api/files/{}'.format(BACKEND_URL, file_name)
            task = requests.get(url_back).json()  
            print("RSLT ==>")
            print(task)
            url_bucket = 'http://{}/api/BucketPo/{}'.format(BUCKET_URL,nfile_name)
            file_path = os.path.join(PROCESS_DIRECTORY, nfile_name)
            with requests.get(url_bucket, stream=True) as r:
                r.raise_for_status()
                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        f.write(chunk)

                    if os.path.exists(file_path):
                        return send_file(file_path, attachment_filename = task['file_name'])
                    else:
                        return {'error': 'Archivo no encontrado'}, 404
        except ConnectionError as e:
            return {'error': 'Api_c getFiles offline -- Connection'}, 404
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            return {'error': 'Api_c getFiles offline -- Timeout'}, 404
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            return {'error': 'Api_c getFiles offline -- ManyRedirects'}, 404
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            return {'error': 'Api_c getFiles offline -- Request'}, 404
        except Exception as e:
            return {'error': 'Api_c getFiles - Error desconocido -' + str(e)}, 404

