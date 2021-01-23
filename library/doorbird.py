import os
import time
import requests
import json

from requests.auth import *


class Doorbird:
    # TODO https
    API_HTTP = "http://{ip}:80/bha-api/{destination}?{search}"
    API_HTTPS = "http://{ip}:80/bha-api/{destination}?{search}"
    IMAGE_HEADER = "data:image/jpeg;base64,{}"

    def __init__(self, ip, username, password):
        self.__ip = ip
        self.__username = username
        self.__password = password

    def make_url(self, destination, image=False, **kwargs):
        if image:
            formula = self.API_HTTP
        else:
            formula = self.API_HTTPS

        url = formula.format(
            ip=self.__ip,
            destination=destination,
            search="&".join(map(lambda a, b: a + "=" + str(b), kwargs.keys(), kwargs.values()))
        )
        return url

    def get_request(self, destination, raw=False, image=False, stream=False, **kwargs):
        response = requests.get(
            url=self.make_url(destination, image, **kwargs),
            auth=HTTPBasicAuth(self.__username, self.__password),
            stream=stream,
            verify=False
        )
        if raw:
            return response
        else:
            return response.content.decode()

    def image_header(self, data):
        return self.IMAGE_HEADER.format(data)

    def live_image(self, coding="base64", resolution="hd", raw=False, without_header=False):
        # TODO sjednotit s take photo, akorát zde dodělat argument - take_photo=False
        """
        :param resolution:
            - 1920x1080/HD  1080p
            - 1280x720      720p
            - 640x480/VGA   480p
        """
        response = self.get_request("image.cgi", raw=raw, image=True, resolution=resolution, format=coding)
        if raw:
            return response.content
        else:
            if without_header:
                return response
            else:
                return self.image_header(response)

    def take_photo(self, directory="user", resolution="hd"):
        directory = os.path.join("doorbird", directory)
        filename = time.strftime("%Y-%m-%d_%H-%M-%S")
        path = os.path.join(directory, f"{filename}.jpg")

        os.makedirs(directory, exist_ok=True)
        with open(path, "wb") as f:
            f.write(self.live_image(coding="unicode", resolution=resolution, raw=True))

        return path

    def open_door(self, relay=1):
        response = self.get_request("open-door.cgi", r=relay)
        result = int(json.loads(response)["BHA"]["RETURNCODE"])
        return result

    def light_on(self):
        response = self.get_request("light-on.cgi")
        result = int(json.loads(response)["BHA"]["RETURNCODE"])
        return result

    def restart(self):
        self.get_request("restart.cgi")
        # TODO response
        return True

    def monitor(self, doorbell=True, motionsensor=True):
        assert doorbell or motionsensor, ValueError("one of arguments must be True")

        search = []
        if doorbell:
            search.append("doorbell")
        if motionsensor:
            search.append("motionsensor")

        return self.get_request("monitor.cgi", raw=True, stream=True, ring=",".join(search))

    def audio_receive(self):  # TODO session id, to samé u ještě něčeho, omrkni to v API_HTTPS
        response = self.get_request("audio-receive.cgi", raw=True, stream=True)
        return response

    def video(self, resolution="1280x720"):
        # TODO rtsp
        
        # Video request:
        #   - FullHD    8.46 FPS
        #   - HD        8.71 FPS
        #   - VGA       8.67 FPS

        # Sequences of images:
        #   - FullHD     8.32 FPS
        #   - HD        10.49 FPS
        #   - VGA       15.15 FPS

        # Coding:       iso-8859-1
        return self.get_request("video.cgi", raw=True, stream=True, resolution=resolution)
