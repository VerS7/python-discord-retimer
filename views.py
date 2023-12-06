"""
Views for discord bot
"""
from typing import Callable

import discord

from discord import Interaction, PartialEmoji, Button


REFRESH_EMJ = PartialEmoji(name="🔄")
DONE_EMJ = PartialEmoji(name="🏁")


class TimerView(discord.ui.View):
    """
    Discord UI Timer View with refresh and stop buttons
    """
    def __init__(self, refresh_action: Callable, stop_action: Callable):
        """
        :param Callable refresh_action: refresh timer function
        :param Callable stop_action: stop timer function
        """
        super().__init__(timeout=None)
        self._refresh_action = refresh_action
        self._stop_action = stop_action

    @discord.ui.button(label="Refresh", custom_id="refresh-btn", style=discord.ButtonStyle.secondary, emoji=REFRESH_EMJ)
    async def refresh_callback(self, ctx: Interaction, button: Button):
        """refresh button callback"""
        self._refresh_action()
        await ctx.response.defer()  # Complete response

    @discord.ui.button(label="Done", custom_id="done-btn", style=discord.ButtonStyle.green, emoji=DONE_EMJ)
    async def end_callback(self, ctx: Interaction, button: Button):
        """stop button callback"""
        self._stop_action()
        await ctx.response.defer()  # Complete response
