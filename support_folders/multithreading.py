"""
                Copyright (C) 2020 Theodoros Siklafidis

    This file is part of GRATIS.

    GRATIS is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    GRATIS is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with GRATIS. If not, see <https://www.gnu.org/licenses/>.
"""

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
