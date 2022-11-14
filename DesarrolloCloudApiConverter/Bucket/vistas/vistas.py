from flask_restful import Resource
from flask import request, send_file
import os
from pprint import pprint
from google.cloud import storage
from lib2to3.pytree import convert
from google.oauth2 import service_account
import json

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

class ManageBucketUP(Resource):
    def post(self, file_name):
        # response = post('/docs/requirementABC', 'requirements.txt', bucket_name)
        #GUARDAR ARCHIVO LOCALMENTE
        file = request.files['file']
        file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
        file.save(file_path)
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob("upfiles/"+file_name)
        blob.upload_from_filename(file_path)
        print('FILE UPLOADED')
        return {'status': 'ok'}, 200

    def get(self, file_name):
        # get('Voice List', r'H:\PythonVenv\GoogleAI\Cloud Storage\Voice List.csv', bucket_name)
        bucket = storage_client.get_bucket(bucket_name)
        file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
        blob = bucket.blob("upfiles/"+file_name)
        blob.download_to_filename(file_path)
        print('FILE DOWNLOADED')
        if os.path.exists(file_path):
            return send_file(file_path, attachment_filename = file_name)
        else:
            return {'status': 'error'}, 404
class ManageBucketPO(Resource):
    def post(self, file_name):
        # response = post('/docs/requirementABC', 'requirements.txt', bucket_name)
        #GUARDAR ARCHIVO LOCALMENTE
        file = request.files['file']
        file_path = os.path.join(PROCESS_DIRECTORY, file_name)
        file.save(file_path)
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob("pofiles/"+file_name)
        blob.upload_from_filename(file_path)
        print('FILE UPLOADED')
        return {'status': 'ok'}, 200

    def get(self, file_name):
        # get('Voice List', r'H:\PythonVenv\GoogleAI\Cloud Storage\Voice List.csv', bucket_name)
        bucket = storage_client.get_bucket(bucket_name)
        file_path = os.path.join(PROCESS_DIRECTORY, file_name)
        blob = bucket.blob("pofiles/"+file_name)
        blob.download_to_filename(file_path)
        print('FILE DOWNLOADED')
        if os.path.exists(file_path):
            return send_file(file_path, attachment_filename = file_name)
        else:
            return {'status': 'error'}, 404

