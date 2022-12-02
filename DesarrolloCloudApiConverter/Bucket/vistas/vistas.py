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
import queue
import threading
import time
import random

url = "https://storage.googleapis.com/bucket_music_file_storage_1/enviroments.json?rand_v="+str(random.randint(1,10000000))
response = urlopen(url)
data = json.loads(response.read())

# cola_upfiles = queue.Queue()
# cola_pofiles = queue.Queue()
cola_bucketfiles = queue.Queue()

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
            file_data = {'file_name': file_name, 'id_task': id_task, 'file_path': file_path, 'bucket': 'UP'}
            cola_bucketfiles.put(file_data)
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
        file_data = {'file_name': file_name, 'id_task': id_task, 'file_path': file_path, 'bucket': 'PO'}
        cola_bucketfiles.put(file_data)
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


# # Funcion para procesar la cola
# def func_upfiles(q, thread_no):
#     while True:
#         file_data = q.get()
#         file_name = file_data['file_name']
#         id_task = file_data['id_task']
#         file_path = file_data['file_path']

#         bucket = storage_client.get_bucket(bucket_name)
#         blob = bucket.blob("upfiles/"+file_name)
#         blob.upload_from_filename(file_path)
#         #print('UP - FILE UPLOADED',flush=True)
#         url_back = 'http://{}/api/taskUpdSt/{}'.format(BACKEND_URI,id_task)
#         actualizar = requests.put(url_back, json={"status":"En Proceso"})
#         #print('UP - TASK UPDATED',flush=True)
#         time.sleep(3)
#         q.task_done()
#         print(f'Thread #{thread_no} processed task #{id_task} in the queue. UPFILE - {file_name}',flush=True)


#         # task = q.get()
#         # time.sleep(2)
#         # q.task_done()
#         # print(f'Thread #{thread_no} is doing task #{task} in the queue.')


# Funcion para procesar la cola
# def func_pofiles(q, thread_no):
#     while True:
#         file_data = q.get()
#         file_name = file_data['file_name']
#         id_task = file_data['id_task']
#         file_path = file_data['file_path']

#         bucket = storage_client.get_bucket(bucket_name)
#         blob = bucket.blob("pofiles/"+file_name)
#         blob.upload_from_filename(file_path)
#         #print('PO - FILE UPLOADED',flush=True)
#         url_back = 'http://{}/api/taskUpd/{}'.format(BACKEND_URI,id_task)
#         actualizar = requests.put(url_back)
#         time.sleep(3)
#         q.task_done()
#         print(f'Thread #{thread_no} processed task #{id_task} in the queue. POFILE - {file_name}',flush=True)

def fun_bucket_files(q, thread_no):
    while True:
        file_data = q.get()
        bucket = file_data['bucket']
        file_name = file_data['file_name']
        id_task = file_data['id_task']
        file_path = file_data['file_path']
        if (bucket == 'UP'):
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob("upfiles/"+file_name)
            blob.upload_from_filename(file_path)
            #print('UP - FILE UPLOADED',flush=True)
            url_back = 'http://{}/api/taskUpdSt/{}'.format(BACKEND_URI,id_task)
            actualizar = requests.put(url_back, json={"status":"En Proceso"})
            #print('UP - TASK UPDATED',flush=True)
            time.sleep(3)
            q.task_done()
            print(f'Thread processed task #{id_task} in the queue. UPFILE - {file_name}',flush=True)
        elif (bucket == 'PO'):         
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob("pofiles/"+file_name)
            blob.upload_from_filename(file_path)
            #print('PO - FILE UPLOADED',flush=True)
            url_back = 'http://{}/api/taskUpd/{}'.format(BACKEND_URI,id_task)
            actualizar = requests.put(url_back)
            time.sleep(3)
            q.task_done()
            print(f'Thread processed task #{id_task} in the queue. POFILE - {file_name}',flush=True)


# Crea 1 worker thread
for i in range(1):
    # worker_upfiles = threading.Thread(target=func_upfiles, args=(cola_upfiles, i,), daemon=True)
    # worker_pofiles = threading.Thread(target=func_pofiles, args=(cola_pofiles, i,), daemon=True)
    # worker_upfiles.start()
    # worker_pofiles.start()
    worker_files_bucket = threading.Thread(target=fun_bucket_files, args=(cola_bucketfiles, i,), daemon=True)
    worker_files_bucket.start()
