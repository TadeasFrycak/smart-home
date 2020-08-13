import datetime
import suntime


class Sun:
    def __init__(self, latitude, longitude):
        self.__latitude = latitude
        self.__longitude = longitude

        self.__sun = suntime.Sun(latitude, longitude)

    @staticmethod
    def get_today_date():
        return datetime.date.today()

    @staticmethod
    def get_time_now():
        return datetime.datetime.now()

    @staticmethod
    def get_time_from_date(date):
        return date.strftime("%H:%M")

    def get_today_sunrise(self):
        return self.__sun.get_local_sunrise_time(self.get_today_date())

    def get_today_sunset(self):
        return self.__sun.get_local_sunset_time(self.get_today_date())

    def day_or_night_now(self):
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
        if user_mode == "smart":
            return self.day_or_night_now()

        else:
            return user_mode
