"""
Main bot file
"""
import discord

from discord import app_commands
from discord import Interaction
from discord.ext import commands

from configs import TOKEN, GUILD_ID, TIMER_TICK_COOLDOWN
from views import TimerView
from embeds import ReTimerEmbed

from retimer import *
from descriptions import *

from loguru import logger


guild = discord.Object(id=GUILD_ID) if GUILD_ID is not None else None
intents = discord.Intents.all()

bot = commands.Bot(command_prefix="/", intents=intents, case_insensitive=False)
command_handler = bot.tree

reTimer = ReTimer(tick_delay=TIMER_TICK_COOLDOWN)


@bot.event
async def on_ready() -> None:
    """Event on bot alive"""
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game("Timing the timings!"))
    logger.info("Bot alive!")


@bot.command(name="sync", description="Sync commands to this Discord Server")
async def tree_sync(ctx: Interaction):
    """
    Syncs command tree to guild
    :param Interaction ctx: discord interaction
    """
    message = await ctx.channel.send("Sync in process...", )
    try:
        await command_handler.sync(guild=guild if guild is not None else ctx.guild)
    except Exception as e:
        await ctx.followup.send("Failed to sync CommandTree to this server.")
        logger.error(f"Can't sync CommandTree to server {ctx.guild.name}", e=e)
        return

    await message.edit(content="Sync to this Server done!")
    logger.info(f"Success link CommandTree to server {ctx.guild.name}")


async def start():
    """start all bot logic"""
    run_bot = asyncio.create_task(bot.start(token=TOKEN))
    run_retimer = asyncio.create_task(reTimer.start())
    await asyncio.gather(run_retimer, run_bot)


if __name__ == '__main__':
    try:
        logger.info("App starting.")
        asyncio.run(start())
    except KeyboardInterrupt:
        logger.info("App exiting.")
