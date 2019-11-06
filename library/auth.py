import subprocess


class Auth:
    def __init__(self):
        pass

    def get_mac(self, ip):
        data = subprocess.check_output(["arp", ip]).decode("utf-8")

        for i in data.split(" "):
            if ":" in i:
                return i

        return None

    def auth(self, ip):
        if str(self.get_mac(ip)) in "TODO":  # TODO
            return True

        else:
            return True
