import unidecode


class PreventHack:
    def __init__(self):
        pass

    @staticmethod
    def make_user_name(first_name, last_name):
        return unidecode.unidecode(first_name).lower() + "." + unidecode.unidecode(last_name).lower()

    def check(self, first_name, last_name, user_name, password, password_repeat, mode, sex, register_date, permission):
        if first_name is None or last_name is None or user_name is None or permission is None or password is None or password_repeat is None or register_date is None or sex is None or mode is None:
            return False

        if first_name in last_name and last_name in first_name:
            return False

        for i in first_name.split(" "):
            if i == "":
                return False

            else:
                if i.strip().capitalize() != i:
                    return False

                if i.isalpha() is not True:
                    return False

                if i in password:
                    return False

        for i in last_name.split(" "):
            if i == "":
                return False

            else:
                if i.strip().capitalize() != i:
                    return False

                if i.isalpha() is not True:
                    return False

                if i in password:
                    return False

        if password != password_repeat:
            return False

        if self.make_user_name(first_name=first_name, last_name=last_name) != user_name:
            return False

        if sex not in ["male", "female"]:
            return False

        if mode not in ["smart", "light", "dark"]:
            return False

        return True
