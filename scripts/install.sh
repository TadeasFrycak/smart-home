# System upgrade
sudo apt update
# sudo apt upgrade
sudo apt dist-upgrade

# MQTT
sudo apt install mosquitto
sudo apt install mosquitto-clients

# Terminal image
sudo apt install catimg

# CV2
sudo apt install ffmpeg
sudo apt install libopenjp2-7
sudo apt install libatlas-base-dev
sudo apt install libilmbase-dev
sudo apt install libopenexr-dev
sudo apt install libgstreamer1.0-dev

# Python
sudo apt install python3
sudo apt install python3-pip

# Python libraries
python3 -m pip install --upgrade pip
python3 -m pip install -r ../requirements.txt
