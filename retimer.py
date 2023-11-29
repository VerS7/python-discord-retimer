"""
ReTimer
Ticks linked to real time from epoch
"""
import re
import asyncio

from time import time
from typing import List, Union, Callable


DONE = "DONE"
TICKING = "TICKING"
PAUSE = "PAUSE"

TIME_PATTERN = re.compile(r'^(\d+d)?:?(\d+h)?:?(\d+m)?$')
TIME_UNITS = {"d": 24 * 60 * 60, "h": 60 * 60, "m": 60}


def get_ctime_s():
    """
    :return: Current time from epoch in seconds
    """
    return int(time())


def validate_time(strtime: str) -> bool:
    """Validates time string with pattern"""
    return bool(TIME_PATTERN.match(strtime))


def time_to_secs(strtime: str) -> int:
    """converts time string to seconds"""
    if not validate_time(strtime):
        raise ValueError("strtime param is incorrect.")
    secs = 0
    for elem in strtime.split(":"):
        for unit, multiplier in TIME_UNITS.items():
            if unit in elem:
                secs += int(elem.replace(unit, "")) * multiplier
    return secs


class Timer:
    """
    Simple timer class
    """
    def __init__(self, name: str, seconds: int, callback: Callable):
        """
        :param str name: timer name
        :param int seconds: positive int of seconds
        :param Callable callback: callback(name, state) function to be called on every tick
        """
        self.name = name
        self.state = TICKING
        self._seconds = seconds
        self._start = get_ctime_s()
        self._end = self._start + self._seconds
        self._callback = callback

    def tick(self):
        """Tick timer."""
        if self._end <= get_ctime_s():
            self.state = DONE
        self._callback(self.name, self.state)


class ReTimer:
    """
    ReTimer class with async ticking loop
    """
    def __init__(self, tick_delay: int):
        self._queue: List[Timer] = []
        self._td = tick_delay

    def add_timer(self, timer: Timer):
        """
        :param Timer timer: adds timer. Raise Exception if timer exists
        """
        if self.get_timer(timer.name) is not None:
            raise Exception("Timer with this name is already ticking.")
        self._queue.append(timer)

    def remove_timer(self, name: str):
        """
        :param str name: removes timer by it name
        """
        timer = self.get_timer(name)
        if timer is None:
            raise Exception("There is no timer with this name in queue.")
        self._queue.remove(timer)

    def get_timer(self, name: str) -> Union[Timer, None]:
        """
        :param str name: name of timer to find
        """
        for timer in self._queue:
            if name == timer.name:
                return timer
        return None

    async def _loop(self):
        while True:
            if len(self._queue) == 0:  # Skip if no timers in queue
                await asyncio.sleep(self._td)
                continue

            for timer in self._queue:
                if timer.state != PAUSE:
                    timer.tick()

                if timer.state == DONE:
                    self._queue.remove(timer)

            await asyncio.sleep(self._td)

    def run(self, event_loop=None):
        """
        :param event_loop: Asyncio event loop
        """
        if event_loop is None:
            event_loop = asyncio.get_event_loop()

        event_loop.run_until_complete(self._loop())
