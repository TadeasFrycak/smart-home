# NOT IN USING
# NOT IN USING
# NOT IN USING
# NOT IN USING
# NOT IN USING
# NOT IN USING
# NOT IN USING
# NOT IN USING
# NOT IN USING
# NOT IN USING
# NOT IN USING
# NOT IN USING
# NOT IN USING
# NOT IN USING
# NOT IN USING
# NOT IN USING
# NOT IN USING


from threading import Thread, Event
import time
import json


class AsynchronousCommunication(Thread):
    """
    Asynchronous communication class
    """

    # Define some constants
    DELAY = 2
    NAMESPACE = "/acom"
    NAME = "tile"

    def __init__(self):
        """
        Init of class AsynCommunication
        """

        super(AsynchronousCommunication, self).__init__()

    def test_generator(self):
        """
        Send some test data to script
        :return:
        """

        while not thread_stop_event.isSet():
            data = arduino.read()
            if data is not None:
                console.print(data)
                console.print(html_json.to_json(data))
                socket_io.emit(self.NAME, json.loads(html_json.to_json(data)),  namespace=self.NAMESPACE)

            time.sleep(0.1)

    def run(self):
        """
        Run Asynchronous Communication
        :return:
        """

        self.test_generator()