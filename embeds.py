"""
Message embeds
"""
from dataclasses import dataclass

from discord import Embed, Member

from retimer import TICKING, DONE, PAUSE
from descriptions import TIMER_DONE_MSG, TIMER_TICKING_MSG, TIMER_PAUSE_MSG


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
    CREATED = 0x43708e
    WARNING = None
    COMPLETE = None
    ALMOST = None
    PROCESS = None
    STANDBY = None


class ReTimerEmbed(Embed):
    """
    ReTimer embed
    """

    def __init__(self, name: str, description: str, author: Member):
        super().__init__(title=name, description=description)
        self.set_author(name=author.name, icon_url=author.avatar.url)
        self.colour = Colors.CREATED
        self.add_field(name="Time", value="Waiting...", inline=True)
        self.add_field(name="State", value="Waiting...", inline=True)

    def update_time(self, time: int):
        self.set_field_at(0, name="Time", value=time, inline=True)

    def update_color(self, color: int):
        pass

    def update_state(self, state: str):
        self.set_field_at(1, name="State", value=state, inline=True)