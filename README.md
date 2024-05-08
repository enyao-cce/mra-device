## Overview
The script janitza-umg96rm-v0.0.1.py takes readings from Janitza UMG 96 RM power meters at 30s intervals. Below are instructions on how to configure the script.

#### Step 1: Copy certificates to 'certs' folder
- Copy client certificates from AWS
- Create a 'certs' folder in the same directory as janitza-umg96rm-v0.x.x.py
- Paste the AWS certificates in the 'certs' folder

#### Step 2: Install dependencies
- Go to terminal
- Enter this command `pip install -r requirements.txt`

#### Step 3: Configure the script
- In terminal, enter command `sudo nano janitza-umg96rm-v0.x.x.py`
- Update broker_address
- Update file paths to ca_cert, client_cert, client_key
- Update the cache length in cache()
- Update topic in publish_message()
- (optional) Call read_registers() for additional devices
	- Change device_id
	- Change label
- Save the changes made
	- Press Ctrl+X
	- Press Y then Enter

#### Step 4: Run the script
- In terminal, enter command `sudo python janitza-umg96rm-v0.x.x.py`
