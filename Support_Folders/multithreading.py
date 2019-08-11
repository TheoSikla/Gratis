__author__ = "Theodoros Siklafidis"
__name__ = "Gratis"
__version__ = "1.0"
__license__ = "GNU General Public License v3.0"

import threading


class StoppableThread(threading.Thread):
    """
        Thread class with a stop() method. The thread itself has to check
        regularly for the stopped() condition.
    """

    def __init__(self, target=None, name=None, args=(), daemon=None):
        super(StoppableThread, self).__init__(target=target, name=name, args=args, daemon=daemon)
        self._stop_event = threading.Event()

        # print(threading.active_count())
        # print(threading.active_count(), self.name)
        # print(threading.enumerate())

    def stop(self):
        self._stop_event.set()
        try:
            self.join()
        except RuntimeError:
            pass

    def isStopped(self):
        return self._stop_event.is_set()
