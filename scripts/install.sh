sudo apt update
sudo apt upgrade -Y
sudo apt install mosquitto -Y
sudo apt install mosquitto-clients -Y
#sudo apt install python3.8 -Y
sudo apt install libopenjp2-7 -Y
sudo apt install libatlas-base-dev -Y
sudo apt install python3 -Y
sudo apt install python3-pip -Y

python3 -m pip install --upgrade pip
python3 -m pip install -r ../requirements.txt
