"""
Message embeds
"""
from dataclasses import dataclass
from typing import Union
from datetime import datetime

from discord import Embed, Member

from .retimer import TICKING, DONE, PAUSE, secs_to_strtime
from .descriptions import TIMER_DONE_MSG, TIMER_TICKING_MSG, TIMER_PAUSE_MSG

STATES = {
    DONE: TIMER_DONE_MSG,
    TICKING: TIMER_TICKING_MSG,
    PAUSE: TIMER_PAUSE_MSG
}


@dataclass
class Colors:
    """
    Embed color types
    """
    CREATED = 0x43708e  # Blue
    WARNING = 0xfbdc3e  # Yellow
    COMPLETE = 0xff2503  # Red
    ALMOST = 0xfb8400  # Orange
    PROCESS = 0xc2c1bf  # Gray
    STANDBY = 0x1ec200  # Green


class ReTimerEmbed(Embed):
    """
    ReTimer embed
    """

    def __init__(self, name: str, description: str, author: Member):
        """
        :param str name: Name displayed on embed
        :param str description: Description displayed on embed
        :param Member author: Server member displayed on embed
        """
        super().__init__(title=f"__{name}__", description=description)
        self.set_author(name=author.name, icon_url=author.avatar.url)
        self.colour = Colors.CREATED
        self.add_field(name="Time", value="Waiting...", inline=True)
        self.add_field(name="State", value="Waiting...", inline=True)

    def update_time(self, time: int):
        """
        Update time on embed with converting to string
        :param int time: seconds
        """
        self.set_field_at(0, name="Time", value=secs_to_strtime(time), inline=True)

    def update_color(self, color: Union[Colors, int]):
        """
        Update embed color
        :param color: HEX color
        """
        self.colour = color

    def update_state(self, state: str):
        """
        Update state on embed
        :param str state: States: TICKING, DONE, PAUSE
        :return:
        """
        self.set_field_at(1, name="State", value=STATES.get(state, "N/A"), inline=True)


class RetimersCommandEmbed(Embed):
    """
    Retimers command embed
    """

    def __init__(self, timers_data: dict):
        """
        :param timers_data: timers data from ReTimer
        """
        super().__init__(title="__Enqueued Timers__")
        self.timestamp = datetime.now()
        self.set_footer(text="\u200b")
        self.colour = Colors.CREATED
        self._register_data(timers_data)

    def _register_data(self, data: dict):
        for info in data.items():
            self.add_field(name=info[0], value=f"State:  {STATES.get(info[1]['state'])}\n"
                                               f"Time:   {info[1]['time']}\n"
                                               f"Remain: {info[1]['time_last']}")
