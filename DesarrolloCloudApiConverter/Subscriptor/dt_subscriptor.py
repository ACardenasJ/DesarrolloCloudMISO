from google.cloud import pubsub_v1
from google.oauth2 import service_account
import json
import uuid
from typing import Any, Callable
import time
from celery import Celery
from redis import Redis

from urllib.request import urlopen
import random
url = "https://storage.googleapis.com/bucket_music_file_storage_1/enviroments.json?rand_v="+str(random.randint(1,10000000))
response = urlopen(url)
data = json.loads(response.read())

REDIS_URI = data['REDIS_URL']
print(url,flush=True)
print(REDIS_URI,flush=True)

celery_app = Celery('tasks', broker='redis://{}/0'.format(REDIS_URI))

@celery_app.task(name="escribir_cola")
def escribir_cola(data):
    pass

project_id = "misonube2022equipo23"
topic_id = "tropico"
subscription_id = "tropico-sub"
with open('dt_creds.json') as source:
    info = json.load(source)



dt_credentials = service_account.Credentials.from_service_account_info(info)
subscriber = pubsub_v1.SubscriberClient(credentials=dt_credentials)
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(msg: pubsub_v1.subscriber.message) -> None:
    print(msg.data,flush=True)
    json_object = json.loads(msg.data)
    #print(json_object["id_task"])
    msg.ack()
    args = (json_object,)
    # AGREGAR MENSAJE A COLA DE MENSAJES
    #print(args)
    escribir_cola.apply_async(args = args)
    time.sleep(5)
    print("Message processed",flush=True)

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n",flush=True)

with subscriber:
    try:
        # streaming_pull_future.result(timeout=timeout)
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.
