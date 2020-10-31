from getmac import get_mac_address
import time


class Clients:
    def __init__(self, server_ip):
        self.__server_ip = server_ip
        self.__clients = []

    # TODO ukládat další info pro stránku s aktivní uživatelé, ... (ban, kick, whitelist, permissions, ...)
    # TODO reconnecting field
    def add_client(self, ip, sid, user_agent, accept_languages, package, referrer, username):
        self.__clients.append(
            {
                "active": True,
                "ip": ip,
                "mac": self.get_mac_from_ip(ip=ip),
                "sid": sid,
                "user": username,
                "user_agent": user_agent,
                "platform": user_agent.platform,
                "browser": {
                    "name": user_agent.browser,
                    "version": user_agent.version,
                    "language": str(accept_languages).split(";")[0],
                    "package": package,
                    "url": referrer,
                },
                "time": {
                    "connected": self.get_time(),
                    "disconnected": None
                }
            }
        )

    def remove_client(self, sid):
        for number, client in enumerate(self.__clients):
            if client["sid"] == sid:
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

    def get_clients(self, active=True):
        clients = []
        for client in self.__clients:
            if not active or (active is True and client["active"] is True):
                clients.append(client)

        return clients


class Refresh:
    def __init__(self, fmng):
        self.__fmng = fmng

    def set_data(self, tab_id, ip, browser, username, slide=None, modal_id=None, modal_type=None, edit=None):
        self.remove_old()

        if self.__fmng.config["refresh"].getboolean("save"):
            if tab_id not in self.get_tab_ids() or username not in self.get_users():
                self.__fmng.refresh_data.append({
                    "device": {
                        "ip": ip,
                        "browser": browser,
                        "tab_id": tab_id
                    },
                    "user": username,
                    "time": time.time(),
                    "data": {
                        "slide": 0,
                        "edit": False,
                        "modal": {
                            "id": False,
                            "type": False
                        }
                    }
                })

            for num, refresh in enumerate(self.__fmng.refresh_data):
                if refresh["device"]["tab_id"] == tab_id and refresh["device"]["ip"] == ip:
                    if refresh["device"]["browser"] == browser and refresh["user"] == username:
                        self.__fmng.refresh_data[num]["time"] = time.time()
                        if slide is not None:
                            self.__fmng.refresh_data[num]["data"]["slide"] = slide

                        if modal_id is not None:
                            self.__fmng.refresh_data[num]["data"]["modal"]["id"] = modal_id

                        if modal_type is not None:
                            self.__fmng.refresh_data[num]["data"]["modal"]["type"] = modal_type

                        if edit is not None:
                            self.__fmng.refresh_data[num]["data"]["edit"] = edit

                        break
            self.__fmng.refresh_data = self.__fmng.refresh_data

    def get_data(self, ip, browser, username):
        self.remove_old()

        probably = []

        for num, refresh in enumerate(self.__fmng.refresh_data):
            if refresh["device"]["ip"] == ip and refresh["device"]["browser"] == browser and refresh["user"] == username:
                self.__fmng.refresh_data[num]["time"] = time.time()
                new_data = refresh["data"].copy()
                new_data["tab_id"] = refresh["device"]["tab_id"]

                probably.append(new_data)

        return probably

    def remove_old(self):
        # TODO QoL remove slide after week, modal after 5min
        for refresh in self.__fmng.refresh_data:
            if (time.time() - refresh["time"]) > self.__fmng.config["refresh"].getint("time"):
                self.__fmng.refresh_data.remove(refresh)

    def get_tab_ids(self):
        tab_ids = []

        for refresh in self.__fmng.refresh_data:
            tab_ids.append(refresh["device"]["tab_id"])

        return tab_ids

    def get_users(self):
        users = []

        for refresh in self.__fmng.refresh_data:
            users.append(refresh["user"])

        return users

    def slide_index_change(self, old_index, new_index):
        for num, refresh in enumerate(self.__fmng.refresh_data):
            if refresh["data"]["slide"] == old_index:
                self.__fmng.refresh_data[num]["data"]["slide"] = new_index

            elif refresh["data"]["slide"] == new_index:
                self.__fmng.refresh_data[num]["data"]["slide"] = old_index
