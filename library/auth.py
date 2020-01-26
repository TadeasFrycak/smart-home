import subprocess


class Auth:
    """
    Auth class
    """

    def __init__(self, fmng, logger):
        """
        Init of class
        :param fmng: file manager
        :param logger: logger
        """

        self.__fmng = fmng
        self.__logger = logger

    def get_mac(self, ip):
        """
        Get MAC address from IP
        :param ip: IP address of user
        :return: MAC address
        """

        data = subprocess.check_output(["arp", ip]).decode("utf-8")

        for i in data.split(" "):
            if ":" in i:
                return i

        return None

    def auth(self, ip, system, browser, header):
        """
        Authenticate
        :param ip: IP of user
        :param system: user´s device system
        :param browser: user´s device browser
        :param header: all header
        :return:
        """

        mac = str(self.get_mac(ip))

        if mac in self.__fmng.whitelist():  # TODO
            return True

        else:
            self.__logger.warning("Access denied for {0} (from {1}) using {3} via {2}, {4}".format(mac, ip, system,
                                                                                                   browser, header))
            return False
