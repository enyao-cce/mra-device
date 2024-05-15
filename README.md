## Overview
The script janitza-umg96rm-v0.0.1.py takes readings from Janitza UMG 96 RM power meters at 30s intervals. The script publish-cache-to-mqtt.py publishes cached messages when internet reconnects. Below are instructions on how to configure the scripts.

#### Step 1: Copy certificates to 'certs' folder
- Copy client certificates from AWS
- Create a 'certs' folder in the same directory as janitza-umg96rm-v0.x.x.py
- Paste the AWS certificates in the 'certs' folder

#### Step 2: Install dependencies
- Go to terminal
- Enter this command `sudo pip install -r requirements.txt`

#### Step 3: Configure the script janitza-umg96rm-v0.x.x.py
- In terminal, enter command `sudo nano janitza-umg96rm-v0.x.x.py`
- Update broker_address
- Update file paths to ca_cert, client_cert, client_key
- Update path to monthly cache in monthly_cache()
- Update path to offline cache in offline_cache()
- Update topic in publish_message()
- (optional) Call read_registers() for additional devices
	- Change device_id
	- Change label
- Save the changes made
	- Press Ctrl+X
	- Press Y then Enter

#### Step 4: Configure the script publish-cache-to-mqtt.py
- In terminal, enter command `sudo nano publish-cache-to-mqtt.py`
- Update broker_address
- Update file paths to ca_cert, cliet_cert, client_key
- Update topic in publish_and_clear_cache()
- Save the changes made
	- Press Ctrl+X
	- Press Y then Enter

#### Step 4: Run the script
- In terminal, enter command `sudo python janitza-umg96rm-v0.x.x.py`
- In a separate terminal, enter command `sudo python publish-cache-to-mqtt.py``
