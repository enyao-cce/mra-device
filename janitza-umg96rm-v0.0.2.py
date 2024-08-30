import ssl
import paho.mqtt.client as mqtt
import time
import schedule
import os
import json
import struct
import minimalmodbus
import requests
import config

broker_address = config.BROKER_ADDRESS
port = 8883

ca_cert = config.CA_CERT
client_cert = config.CLIENT_CERT
client_key = config.CLIENT_KEY

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Connection failed with error code " + str(rc))
    print ()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.tls_set(ca_cert, certfile=client_cert, keyfile=client_key, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
client.connect(broker_address, port, keepalive=5)
client.loop_start()

while not client.is_connected():
    time.sleep(1)

message = {}

def read_registers(device_port, device_id, register_dict, label, fc=3):
    instrument = minimalmodbus.Instrument(device_port, device_id)
    instrument.serial.baudrate = 9600
    instrument.serial.timeout = 1

    global message

    try:
        for key, value in register_dict.items():
            reg = instrument.read_registers(int(value), 2, functioncode=fc)
            float_value = struct.unpack('>f', struct.pack('>HH', reg[0], reg[1]))[0]
            message[f"{label}_{key}"] = float_value
    except Exception as e:
        print(f"Error: {e}")

def is_internet_available():
    try:
        res = requests.get('https://www.google.com', timeout=5)
        return res.status_code == 200
    except requests.exceptions.Timeout:
        return False
    except requests.ConnectionError:
        return False

def monthly_cache():
     with open(config.MONTHLY_CACHE, 'r+') as f:
        cache = json.load(f)
        thirty_days_ago = int(time.time() * 1000) - (30 * 24 * 60 * 60 * 1000)
        cache = [entry for entry in cache if entry['state']['reported']['timestamp'] > thirty_days_ago]
        cache.append(message)
        f.seek(0)
        json.dump(cache, f)
        f.truncate()
     print ("Added message to monthly cache:\n", message)

def offline_cache():
    if is_internet_available() and client.is_connected():
        print ("Mqtt connection is available. No need to add message to offline cache")
        return
    with open(config.OFFLINE_CACHE, 'r+') as f:
        cache = json.load(f)
        thirty_days_ago = int(time.time() * 1000) - (30 * 24 * 60 * 60 * 1000)
        cache = [entry for entry in cache if entry['state']['reported']['timestamp'] > thirty_days_ago]
        cache.append(message)
        f.seek(0)
        json.dump(cache, f)
        f.truncate()
    print ("Added message to offline cache:\n", message)

def publish_message():
    topic = config.TOPIC

    global message
    message = {"state": {"reported": message}}

    client.publish(topic, json.dumps(message))
    print("Published message:\n", message)

def sequence():
    port = '/dev/ttyUSB0'
    registers = {
        "voltL1-N": 19000,
        "voltL2-N": 19002,
        "voltL3-N": 19004,
        "voltL1-L2": 19006,
        "voltL2-L3": 19008,
        "voltL1-L3": 19010,
        "currL1": 19012,
        "currL2": 19014,
        "currL3": 19016,
        "vecIN": 19018,
        "realP1": 19020,
        "realP2": 19022,
        "realP3": 19024,
        "realPsum3": 19026,
        "apparentS1": 19028,
        "apparentS2": 19030,
        "apparentS3": 19032,
        "apparentSsum3": 19034,
        "frequency": 19050
    }

    global message
    message = {"timestamp": int(time.time()*1000)}

    read_registers(port, 1, registers, 'testlabel')
    publish_message()
    monthly_cache()
    offline_cache()

    print ()

schedule.every().minute.at(":00").do(sequence)
schedule.every().minute.at(":30").do(sequence)

while True:
    schedule.run_pending()
    time.sleep(1)
