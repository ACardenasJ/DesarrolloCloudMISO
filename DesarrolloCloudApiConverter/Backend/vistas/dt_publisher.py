from google.cloud import pubsub_v1
from google.oauth2 import service_account
import json
import uuid
from typing import Any, Callable
from concurrent import futures

project_id = "misonube2022equipo23"
topic_id = "tropico"
with open('./vistas/dt_creds.json') as source:
    info = json.load(source)

dt_credentials = service_account.Credentials.from_service_account_info(info)

publisher = pubsub_v1.PublisherClient(credentials=dt_credentials)
topic_path = publisher.topic_path(project_id, topic_id)

# Publish messages to the topic

topic_path = publisher.topic_path(project_id, topic_id)
publisher = pubsub_v1.PublisherClient(credentials=dt_credentials)
publish_futures = []

def get_callback(
    publish_future: pubsub_v1.publisher.futures.Future, data: str
) -> Callable[[pubsub_v1.publisher.futures.Future], None]:
    def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
        try:
            # Wait 60 seconds for the publish call to succeed.
            print(publish_future.result(timeout=60))
        except futures.TimeoutError:
            print(f"Publishing {data} timed out.")

    return callback

class publicador():
    def publish_sms(self, data):
        js_str = json.dumps(data).encode("utf-8")
        print(js_str)
        # When you publish a message, the client returns a future.
        publish_future = publisher.publish(topic_path, js_str)
        # Non-blocking. Publish failures are handled in the callback function.
        publish_future.add_done_callback(get_callback(publish_future, data))
        publish_futures.append(publish_future)
        futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)
        print("All messages published.")