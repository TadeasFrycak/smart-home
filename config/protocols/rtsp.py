import base64
import random
import string
import time
from threading import Thread

import numpy as np

from config.protocols.default import Protocol
from flask_babel import gettext
from multiprocessing import Process
import ctypes
import multiprocessing
import cv2 as cv
import gipc


class RTSPProcess(Process):
    def __init__(self, content, url):
        super().__init__()
        self.__content = content
        self.__url = url
        self.__running = multiprocessing.Value("b", 1)

    def close(self):
        # with self.__running.get_lock():
        print("zavírám2")
        self.__running.value = 0

    def run(self):
        # TODO tohle nesmí být threadové, bude to zbytečně zasekávat server, to stejné zvonek  mqtt
        print("rtsp://" + self.__url)
        capture = cv.VideoCapture("rtsp://" + self.__url)

        while self.__running:
            # time.sleep(0.05)
            ret, frame = capture.read()
            frame = cv.resize(frame, (640, 480))
            frame = frame.reshape(480*640*3)

            if frame is None:
                continue

            self.__content[:] = frame


class RTSPThread(Thread):
    def __init__(self, terminal, general, url):
        super().__init__()
        self.__terminal = terminal
        self.__general = general
        self.__url = url

        self.__running = True

        self.__content = multiprocessing.Array("i", 640*480*3)

        self.__process = RTSPProcess(self.__content, url)
        self.__process.start()

    def close(self):
        # with self.__running.get_lock():
        print("zavírám1")
        self.__process.close()
        self.__running = False

    def run(self):
        while True:
            time.sleep(0.6)

            content = np.array(self.__content[:]).reshape(480, 640, 3)
            encoded = cv.imencode(".jpg", content)[1].tobytes()
            base64_encoded = base64.b64encode(encoded).decode("utf-8")
            content = "data:image/jpeg;base64,{}".format(base64_encoded)

            if self.__running:
                self.__general.update(protocol_type="rtsp", value=content, config_part={"url": self.__url},
                                      save=False)
            else:
                self.__general.update(protocol_type="rtsp", value=content, config_part={"url": self.__url})
                break


class RTSP(Protocol):
    TYPE = "rtsp"
    VISIBLE = True
    NAME = gettext("RTSP")

    __PREPEND = "rtsp://"

    def __init__(self, terminal, update):
        super().__init__(terminal, update)

        self.__threads = {}

    def config(self):
        return {
            self._URL: "<user>:<password>@<IP>:554/Streaming/Channels/<camera>02"
        }

    def edit_config(self):
        from config.items.input import Input

        return {
            self._URL: Input().make_object(value=self.config()[self._URL], prepend=self.__PREPEND, button=True, label=gettext("RTSP URL"), max_length=80),
        }

    def add_listener_inner(self, config):
        url = config[self._URL]

        thread = RTSPThread(terminal=self._terminal, general=self._general, url=url)
        thread.start()

        self.__threads[url] = thread

    def remove_listener_inner(self, config):
        url = config[self._URL]

        self.__threads[url].close()
        del self.__threads[url]
