from flask_login import current_user
from getmac import get_mac_address
from flask import request
import time


class Clients:
    def __init__(self, server_ip):
        self.__server_ip = server_ip
        self.__clients = []

    # TODO ukládat další info pro stránku s aktivní uživatelé, ... (ban, kick, whitelist, permissions, ...)
    # TODO reconnecting field
    def add_client(self):
        user_agent = request.user_agent
        ip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)

        if current_user.is_authenticated:
            username = current_user.username

        else:
            username = None

        self.__clients.append(
            {
                "active": True,
                "ip": ip,
                "mac": self.get_mac_from_ip(ip=ip),
                "sid": request.sid,
                "user": username,
                "user_agent": user_agent,
                "platform": user_agent.platform,
                "browser": {
                    "name": user_agent.browser,
                    "version": user_agent.version,
                    "language": str(request.accept_languages).split(";")[0],
                    "package": request.headers.get("X-Requested-With", None),
                    "url": request.referrer,
                },
                "time": {
                    "connected": self.get_time(),
                    "disconnected": None
                }
            }
        )

    def remove_client(self):
        for number, client in enumerate(self.__clients):
            if client["sid"] == request.sid:
                self.__clients[number]["active"] = False
                self.__clients[number]["time"]["disconnected"] = self.get_time()

    @staticmethod
    def get_time():
        return time.strftime("%d.%m.%Y %H:%M:%S UTC", time.gmtime())  # TODO localize time pomocí flask_babel

    def get_clients_sid(self, active=True):
        sids = []
        for client in self.__clients:
            if not active or (active is True and client["active"] is True):
                sids.append(client["sid"])

        return sids

    def get_mac_from_ip(self, ip):
        if self.__server_ip == ip:
            return get_mac_address(hostname="localhost")
        else:
            return get_mac_address(ip=ip)

    def get_clients(self, active=True, convert_time=True):
        clients = []
        for client in self.__clients:
            if not active or (active is True and client["active"] is True):
                clients.append(client)

        return clients
