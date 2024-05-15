import ssl
import paho.mqtt.client as mqtt
import time
import schedule
import os
import json
import requests

cache_file = 'offline_cache.json'

broker_address = "mqtt.example.com"
port = 8883

ca_cert = "path/to/ca_cert"
client_cert = "path/to/client_cert"
client_key = "path/to/client_key"

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Connection failed with error code " + str(rc))

def is_internet_available():
    try:
        res = requests.get('https://www.google.com', timeout=5)
        return res.status_code == 200
    except requests.exceptions.ReadTimeout:
        print ("Internet connection check timed out.")
        return False
    except requests.ConnectionError:
        return False

def publish_and_clear_cache():
    if not is_internet_available():
        print ('Internet is not available. Skipping publish.\n')
        return

    with open(cache_file, 'r') as f:
        cache = json.load(f)

    if len(cache) == 0:
        print (f"{cache_file} is empty. Nothing to publish.\n")
        return

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.tls_set(ca_cert, certfile=client_cert, keyfile=client_key, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
    client.connect(broker_address, port)
    client.loop_start()

    while not client.is_connected():
        time.sleep(1)

    while client.is_connected() and len(cache) > 0:
        message = cache.pop(0)
        topic = "topic/subtopic"
        client.publish(topic, json.dumps(message))

        print (f"Published message:\n {message}\n")

        with open(cache_file, 'w') as f:
            json.dump(cache, f)

    client.disconnect()

schedule.every(5).seconds.do(publish_and_clear_cache)

while True:
    schedule.run_pending()
    time.sleep(1)
