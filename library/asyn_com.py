from threading import Thread, Event


class AsynchronousCommunication(Thread):
    """
    Asynchronous communication class
    """

    # Define some constants
    DELAY = 2
    NAMESPACE = "/acom"
    NAME = "test"

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

        # while not thread_stop_event.isSet():
        # while not thread_stop_event.isSet():
        # if random.choice([0, 1]) == 1:
        #    socket_io.emit(self.NAME, {"id": random.choice(
        #        ["toggle-1", "toggle-2", "toggle-3", "toggle-4", "toggle-6", "toggle-7", "toggle-8", "toggle-9"]),
        #                               "value": random.randint(0, 1)}, namespace=self.NAMESPACE)

        # else:
        #    socket_io.emit(self.NAME, {"id": random.choice(
        #        ["percentage-1", "percentage-2", "percentage-3", "percentage-4", "percentage-5"]),
        #                               "value": random.randint(0, 100)}, namespace=self.NAMESPACE)
        # socket_io.emit(self.NAME, {"id": "toggle-" + str(random.randint(100, 200)),
        #                           "value": random.randint(0, 1)}, namespace=self.NAMESPACE)
        # time.sleep(self.DELAY)

    def run(self):
        """
        Run Asynchronous Communication
        :return:
        """

        self.test_generator()