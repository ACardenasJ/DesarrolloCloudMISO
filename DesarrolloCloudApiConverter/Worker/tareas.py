from celery import Celery
import requests
from time import sleep
import json
#from decouple import config
from urllib.request import urlopen

import random
url = "https://storage.googleapis.com/bucket_music_file_storage_1/enviroments.json?rand_v="+str(random.randint(1,10000000))
response = urlopen(url)
data = json.loads(response.read())

CONVERTER_URI = data['CONVERTER_URL']
BACKEND_URI = data['BACKEND_URL']
REDIS_URI = data['REDIS_URL']
print(url,flush=True)
print(CONVERTER_URI,flush=True)
print(BACKEND_URI,flush=True)
print(REDIS_URI,flush=True)


celery = Celery(__name__, broker='redis://{}/0'.format(REDIS_URI))

def reintegrar_cola(str_data):
    #AGREGA A LA COLA DE TAREAS
    args = (str_data,)
    escribir_cola.apply_async(args = args)


@celery.task(name="escribir_cola")
def escribir_cola(data):
    #print(data)
    
    # with open('log_registrar_info.txt','a+') as file:
    #     file.write('{}\n'.format(data))

    try:
        task_info = requests.get('http://{}/api/task/{}'.format(BACKEND_URI,data["id_task"])).json()
        if task_info["status"] == "Pendiente":
            #print("PENDING")
            sleep(1)
            reintegrar_cola(data)
        elif task_info["status"] == "En Proceso":
            rslt = requests.get('http://{}/api/status'.format(CONVERTER_URI))
            #print(rslt)
            if rslt.status_code == 200:
                requests.post('http://{}/api/convertidor'.format(CONVERTER_URI), json=data)
            else:
                reintegrar_cola(data)
        else:
            print("ERROR")
            sleep(1)
            reintegrar_cola(data)
    except requests.exceptions.ConnectionError as r:
        r.status_code = "Connection refused"
        print(r.status_code)
        print(r)
        reintegrar_cola(data)
        sleep(2)

