# System upgrade
sudo apt update
# sudo apt upgrade
sudo apt dist-upgrade

# MQTT
sudo apt install mosquitto mosquitto-clients

# Terminal image
sudo apt install catimg

# CV2
sudo apt install ffmpeg libatlas-base-dev libopenjp2-7 libgstreamer1.0-dev libgtk-3-0 libopenexr-dev libilmbase-dev

# Python
sudo apt install python3 python3-pip python3-venv python3-dev

#sudo apt install uwsgi
sudo apt install nginx
sudo apt install ufw
# sudo apt install software-properties-common  # add-apt-repository
# sudo add-apt-repository ppa:certbot/certbot
# sudo apt install python-certbot-nginx  # certificate SSL

# sudo apt install python3-numpy python3-gevent python3-pil python3-opencv
# Python libraries
python3 -m pip install --upgrade pip
python3 -m pip install -r ../requirements.txt
