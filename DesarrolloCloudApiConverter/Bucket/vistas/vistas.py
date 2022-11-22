from flask_restful import Resource
from flask import request, send_file
import os
from pprint import pprint
from google.cloud import storage
from lib2to3.pytree import convert
from google.oauth2 import service_account
import json
import requests
from urllib.request import urlopen
import time

import random
url = "https://storage.googleapis.com/bucket_music_file_storage_1/enviroments.json?rand_v="+str(random.randint(1,10000000))
response = urlopen(url)
data = json.loads(response.read())

BACKEND_URI = data['BACKEND_URL']
print(url,flush=True)
print(BACKEND_URI,flush=True)

project_id = "misonube2022equipo23"
UPLOAD_DIRECTORY = "./vistas/upfiles/"
PROCESS_DIRECTORY = "./vistas/pofiles/"
with open('bucket_creds.json') as source:
    info = json.load(source)

storage_credentials = service_account.Credentials.from_service_account_info(info)
storage_client = storage.Client(project=project_id, credentials=storage_credentials)
bucket_name = 'bucket_music_file_storage-1'

class statusCheck(Resource):
    def get(self):
        return {'status': 'ok'}, 200

class MBucketPOST(Resource):
    def post(self, file_name, id_task):
            # response = post('/docs/requirementABC', 'requirements.txt', bucket_name)
            #GUARDAR ARCHIVO LOCALMENTE
            file = request.files['file']
            file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
            file.save(file_path)
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob("upfiles/"+file_name)
            blob.upload_from_filename(file_path)
            print('FILE UPLOADED')
            url_back = 'http://{}/api/taskUpdSt/{}'.format(BACKEND_URI,id_task)
            actualizar = requests.put(url_back, json={"status":"En Proceso"})
            print('TASK UPDATED')
            time.sleep(3)
            return {'status': 'ok'}, 200

class ManageBucketUP(Resource):
    def get(self, file_name):
        # get('Voice List', r'H:\PythonVenv\GoogleAI\Cloud Storage\Voice List.csv', bucket_name)
        bucket = storage_client.get_bucket(bucket_name)
        file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
        if os.path.exists(file_path):
            return send_file(file_path, attachment_filename = file_name)
        else:
            blob = bucket.blob("upfiles/"+file_name)
            blob.download_to_filename(file_path)
            print('FILE DOWNLOADED')
            if os.path.exists(file_path):
                return send_file(file_path, attachment_filename = file_name)
            else:
                return {'status': 'error'}, 404
class ManageBucketPOST2_(Resource):
    def post(self, file_name,id_task):
        # response = post('/docs/requirementABC', 'requirements.txt', bucket_name)
        #GUARDAR ARCHIVO LOCALMENTE
        file = request.files['file']
        file_path = os.path.join(PROCESS_DIRECTORY, file_name)
        file.save(file_path)
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob("pofiles/"+file_name)
        blob.upload_from_filename(file_path)
        print('FILE UPLOADED')
        url_back = 'http://{}/api/taskUpd/{}'.format(BACKEND_URI,id_task)
        actualizar = requests.put(url_back)
        time.sleep(3)
        return {'status': 'ok'}, 200


class ManageBucketPO(Resource):
    def get(self, file_name):
        # get('Voice List', r'H:\PythonVenv\GoogleAI\Cloud Storage\Voice List.csv', bucket_name)
        bucket = storage_client.get_bucket(bucket_name)
        file_path = os.path.join(PROCESS_DIRECTORY, file_name)
        if os.path.exists(file_path):
            return send_file(file_path, attachment_filename = file_name)
        else:
            blob = bucket.blob("pofiles/"+file_name)
            blob.download_to_filename(file_path)
            print('FILE DOWNLOADED')
            if os.path.exists(file_path):
                return send_file(file_path, attachment_filename = file_name)
            else:
                return {'status': 'error'}, 404

