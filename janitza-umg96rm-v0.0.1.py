import ssl
import paho.mqtt.client as mqtt
import time
import schedule
import os
import json
import struct
import minimalmodbus

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
    print ()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.tls_set(ca_cert, certfile=client_cert, keyfile=client_key, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
client.connect(broker_address, port)
client.loop_start()

while not client.is_connected():
    time.sleep(1)

message = {}

def read_registers(device_port, device_id, register_dict, label):
    instrument = minimalmodbus.Instrument(device_port, device_id)
    instrument.serial.baudrate = 9600
    instrument.serial.timeout = 1

    global message
    message = {"timestamp": int(time.time()*1000)}

    try:
        for key, value in register_dict.items():
            reg = instrument.read_registers(int(value), 2, functioncode=3)
            float_value = struct.unpack('>f', struct.pack('>HH', reg[0], reg[1]))[0]
            message[f"{label}_{key}"] = float_value
    except Exception as e:
        print(f"Error: {e}")

def cache():
    with open('cache.json', 'r+') as f:
        data = json.load(f)
        if len(data) == 5:
            data.pop(0)
        data.append(message)
        f.seek(0)
        json.dump(data, f)
        f.truncate()

    print ("Cached message:\n", message)

def publish_message():
    topic = "topic/subtopic"

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
        "apparentSsum3": 19034
    }
    read_registers(port, 1, registers, 'example_label')
    publish_message()
    cache()

    print ()

schedule.every().minute.at(":00").do(sequence)
schedule.every().minute.at(":30").do(sequence)

while True:
    schedule.run_pending()
    time.sleep(1)
