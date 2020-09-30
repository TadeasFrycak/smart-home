import unidecode


class PreventHack:
    def __init__(self):
        pass

    @staticmethod
    def hacker():
        print("POZOR POZOR HACKER")

    def check(self, first_name, last_name, username, password):
        """
        Check from hack
        :param first_name:
        :param last_name:
        :param username:
        :param password:
        :return: True/False
        """

        if first_name is None or last_name is None or username is None or password is None:
            return False

        # if first_name in last_name and last_name in first_name:
        #     return False

        # for i in first_name.split(" "):
        #    if i == "":
        #        return False
        #
        #    else:
        #        if i.strip().capitalize() != i:
        #            return False
        #
        #        if i.isalpha() is not True:
        #            return False
        #
        #        if i in password:
        #            return False

        if unidecode.unidecode(username) != username:
            return False

        return True
