"""
ReTimer
Ticks linked to real time from epoch
"""
import re
import asyncio

from time import time
from typing import List, Union, Callable, Optional, Dict


DONE = "DONE"
TICKING = "TICKING"
PAUSE = "PAUSE"

TIME_PATTERN = re.compile(r'^(\d+d)?:?(\d+h)?:?(\d+m)?$')
TIMING_PATTERN = re.compile(r'^(\d+d)?:?(\d+h)?:?(\d+m)?-[^/]*$')
TIME_UNITS = {"d": 24 * 60 * 60, "h": 60 * 60, "m": 60}


def get_ctime_s():
    """
    :return int: Current time from epoch in seconds
    """
    return int(time())


def validate(string: str, pattern: re.Pattern) -> bool:
    """
    Validates string with pattern
    :param string string: string to validate
    :param Pattern pattern: regex pattern
    :return bool:
    """
    return bool(pattern.match(string))


def str_to_timings(strtimings: str) -> Dict[int, str]:
    """
    Converts timing string to timings dict
    :param str strtimings: str with timings like 1h:-an hour, 3h:30m-A lot of time
    :return Dict[int, str]: dict of seconds and timing descriptions
    """
    timings = {}
    for timing in strtimings.split(", "):
        if validate(timing, TIMING_PATTERN) is False:
            raise ValueError("Timings string is incorrect.")
        strtime, description = timing.split("-")
        timings[time_to_secs(strtime)] = description
    return timings


def time_to_secs(strtime: str) -> int:
    """
    Converts time string to seconds
    :param str strtime: time string
    :return int: seconds
    """
    if not validate(strtime, TIME_PATTERN):
        raise ValueError("strtime param is incorrect.")
    secs = 0
    for elem in strtime.split(":"):
        for unit, multiplier in TIME_UNITS.items():
            if unit in elem:
                secs += int(elem.replace(unit, "")) * multiplier
    return secs


def secs_to_strtime(secs: int) -> str:
    """
    Convert seconds to time string
    :param int secs: seconds
    :return str: pretty time string
    """
    if secs < 0:
        secs = 0

    hours, remain = divmod(secs, 3600)
    minutes, seconds = divmod(remain, 60)

    time_string = ""
    if hours > 0:
        time_string += f"{hours}h:"
    if minutes > 0:
        time_string += f"{minutes}m:"
    if seconds > 0 or not time_string:
        time_string += f"{seconds}s"

    return time_string.rstrip(':')


class Timer:
    """
    Simple timer class
    """
    __slots__ = ["name", "state", "seconds", "start", "end",
                 "_base_timings", "_timings", "_callback"]

    def __init__(self, name: str, seconds: int,
                 callback: Callable[[str, str, int, Union[str, None]], None],
                 timings: Optional[dict] = None):
        """
        :param str name: timer name
        :param int seconds: positive int of seconds
        :param callback: callback(name, state, seconds_remain, Description/None)
                         function to be called on every tick
        """
        self.name = name
        self.state = TICKING
        self.seconds = seconds
        self.start = get_ctime_s()
        self.end = self.start + self.seconds
        self._base_timings = timings
        self._timings = self._create_timings(self._base_timings)
        self._callback = callback

    @property
    def last(self):
        """
        :return int: Seconds to last tick
        """
        return self.end - get_ctime_s()

    def _create_timings(self, timings: Dict[int, str]) -> Union[Dict[int, str], Dict]:
        """Create real timing compare to timer end with description"""
        if timings is not None:
            return {self.end - elem[0]: elem[1] for elem in timings.items()}
        return {}

    def reload(self):
        """Reload this timer to start condition"""
        self.state = TICKING
        self.start = get_ctime_s()
        self.end = self.start + self.seconds
        self._timings = self._create_timings(self._base_timings)

    def done(self):
        """Set state to DONE"""
        self.state = DONE

    def tick(self):
        """Tick timer"""
        current_time = get_ctime_s()
        if self.end <= current_time:
            self.state = DONE

        if not self._timings or len(self._timings) == 0:
            self._callback(self.name, self.state, self.last, None)
            return

        for timing in self._timings.items():
            if timing[0] <= current_time:
                self._callback(self.name, self.state, self.last, timing[1])  # Callback with timing
                self._timings.pop(timing[0])
                return
        self._callback(self.name, self.state, self.last, None)


class ReTimer:
    """
    ReTimer class with async ticking loop
    """
    def __init__(self, tick_delay: int):
        self._queue: List[Timer] = []
        self._td = tick_delay

    @property
    def timers(self):
        """
        :return: All enqueued timers
        """
        return self._queue

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

    def run(self, event_loop: asyncio.AbstractEventLoop = None):
        """
        Blocking call. Use only if ReTimer loop is only one blocking non-ending loop
        :param event_loop: Asyncio event loop
        """
        if event_loop is None:
            event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(self._loop())

    async def start(self):
        """async _loop wrapper"""
        return await self._loop()
