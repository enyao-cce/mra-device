## Overview
Data is fetched from a Janitza UMG96RM power meter at 30s intervals using the [minimalmodbus]('https://minimalmodbus.readthedocs.io/en/stable/') library and published to a MQTT broker using the [paho-mqtt]('https://eclipse.dev.paho/files/paho.mqtt.python/html/client.html') library.

At the same time, data is stored in 2 caches - monthly, offline. The offline cache only stores data when there is no internet.

When internet resumes, the data in the offline cache gets published to the MQTT broker.

Below are instructions on how to setup the python scripts.

## Setup Guide

#### Step 1: MQTT client authentication using SSL certs
* Download client certificate, private key, and root CA certificate from AWS IoT console
* Create a new 'certs' folder in the same directory as janitza-umg96rm-v0.x.x.py
* Place the AWS certificates in the 'certs' folder

#### Step 2: Install dependencies
```
pip install -r requirements.txt
```

#### Step 3: Update your settings in config.py
```
sudo nano config.py
```

#### Step 4: Run the python scripts
```
sudo python janitza-umg96rm-v0.x.x.py
```
Open a new terminal and run
```
sudo python publish-cache-to-mqtt.py
```

## Additional Information

#### Autostart python scripts using systemd (Recommended)
Create a new service
```
sudo nano /etc/systemd/system/name-of-your-service.service
```
Paste the following into the file
```
[Unit]
Description=name-of-your-service Service
After=multi-user.target

[Service]
Type=idle
User=pi
ExecStart=/usr/bin/python3 /home/pi/your-Python-script.py
Restart=always

[Install]
WantedBy=multi-user.target
```
Save the file with Ctrl+X, press Y then press Enter<br><br><br>
Change the file permissions
```
sudo chmod 644 /etc/systemd/system/name-of-your-service.service
```
Update the system
```
sudo systemctl daemon-reload
sudo systemctl enable name-of-your-service.service
```
Reboot the system
```
sudo reboot
```

#### Fetch data from multiple devices
Edit janitza-umg96rm-v0.x.x.py
```
sudo nano janitza-umg96rm-v0.x.x.py
```
Scroll down until you see the sequence() function <br>

Call read_registers() in the line after the existing one and change the following parameters:
```
device_id
label
```
Save the file with Ctrl+X, press Y then press Enter <br>

#### Check cache
To print all rows
```
python check_cache.py monthly_cache.json
```
To print the latest 5 elements
```
python check_cache.py monthly_cache.json -latest 5
```
Where `latest` specifies the most recent number of rows to display <br><br>
This also applies to `offline_cache.json`

#### Reset cache
Example usage
```
python reset_cache.py monthly_cache.json
```
This also applies to `offline_cache.json`

## Precaution
1. **Do not rename the cache files, they are used for reference**<br>
2. **Ensure cache files only contain either an empty list or a list of dictionary items**
