import os
import time
import requests
import json

from requests.auth import *


class Doorbird:
    # TODO https
    API_HTTP = "http://{ip}:80/bha-api/{destination}?{search}"
    API_HTTPS = "https://{ip}:443/bha-api/{destination}?{search}"
    IMAGE_HEADER = "data:image/jpg;base64,{}"

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

    def live_image(self, coding="base64", resolution="hd", raw=False):
        response = self.get_request("image.cgi", raw=raw, image=True, resolution=resolution, format=coding)
        if raw:
            return response.content
        else:
            return self.IMAGE_HEADER.format(response)

    def take_photo(self, directory="user"):
        directory = os.path.join("doorbird", directory)
        filename = time.strftime("%Y-%m-%d_%H-%M-%S")
        path = os.path.join(directory, f"{filename}.jpg")

        os.makedirs(directory, exist_ok=True)
        with open(path, "wb") as f:
            f.write(self.live_image(coding="unicode", raw=True))

    def open_door(self, relay=1):
        response = self.get_request("open-door.cgi", r=relay)
        result = int(json.loads(response)["BHA"]["RETURNCODE"])
        return result

    def light_on(self):
        response = self.get_request("light-on.cgi")
        result = int(json.loads(response)["BHA"]["RETURNCODE"])
        return result

    def monitor(self, doorbell=True, motionsensor=True):
        assert doorbell or motionsensor, ValueError("one of arguments must be True")

        search = []
        if doorbell:
            search.append("doorbell")
        if motionsensor:
            search.append("motionsensor")
        response = self.get_request("monitor.cgi", raw=True, stream=True, ring=",".join(search))
        return response

    def audio_receive(self):  # TODO session id, to samé u ještě něčeho, omrkni to v API_HTTPS
        response = self.get_request("audio-receive.cgi", raw=True, stream=True)
        return response
