import datetime
import suntime


class Sun:
    """
    Sun class
    """

    def __init__(self, latitude, longitude):
        """
        Init of Sun class
        """

        assert isinstance(latitude, int) or isinstance(latitude, float), "latitude should be int or float"
        assert isinstance(longitude, int) or isinstance(longitude, float), "longitude should be int or float"

        self.__latitude = latitude
        self.__longitude = longitude

        self.__sun = suntime.Sun(latitude, longitude)

    @staticmethod
    def get_today_date():
        """
        Get today date
        :return: today date
        """

        return datetime.date.today()

    @staticmethod
    def get_time_now():
        """
        Get actual time
        :return: time now
        """

        return datetime.datetime.now()

    @staticmethod
    def get_time_from_date(date):
        """
        Format date to get time
        :param date: date
        :return: time
        """

        return date.strftime("%H:%M")

    def get_today_sunrise(self):
        """
        Get today sunrise
        :return: today sunrise
        """

        return self.__sun.get_local_sunrise_time(self.get_today_date())

    def get_today_sunset(self):
        """
        Get today sunset
        :return: today sunset
        """

        return self.__sun.get_local_sunset_time(self.get_today_date())

    def day_or_night_now(self):
        """
        Is day or night now?
        :return: light/dark
        """

        sunrise = self.get_today_sunrise().time()
        sunset = self.get_today_sunset().time()
        time = self.get_time_now().time()

        if sunset >= time > sunrise:
            return "light"

        elif time > sunset > sunrise or sunrise >= time:
            return "dark"

        else:
            print("SUN FATAL ERROR")
            return None

    def get_mode(self, user_mode):
        """
        Get mode from user mode
        :param user_mode: user mode
        :return: mode
        """

        if user_mode == "smart":
            return self.day_or_night_now()

        else:
            return user_mode
