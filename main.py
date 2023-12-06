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


@command_handler.command(name="retime", description=RETIME_DESCRIPTION, guild=guild)
@app_commands.describe(name=RETIME_ARG_NAME, about=RETIME_ARG_DESCRIPTION, time=RETIME_ARG_TIME,
                       role=RETIME_ARG_ROLE, timings=RETIME_ARG_TIMINGS)
async def retime(ctx: Interaction, name: str, about: str, time: str, role: discord.Role, timings: str):
    """
    /retime command
    :param Interaction ctx: discord interaction
    -- Command args --
        :param str name: Name of timer
        :param str about: Description of timer
        :param str time: Time to timer tick
        :param Role role: Role to notice
        :param str timings: Timings with description when timer will notice
    """
    try:
        secs = time_to_secs(time)
        timings = str_to_timings(timings)
    except ValueError:
        logger.exception(f"Wrong args. {time} / {timings}")
        return

    except Exception as e:
        logger.error("ReTime command error.", e=e)
        return

    embed = ReTimerEmbed(name, about, ctx.user)
    view = TimerView(refresh_action=lambda: reTimer.get_timer(name).reload(),
                     stop_action=lambda: reTimer.get_timer(name).done())

    await ctx.response.send_message(embed=embed, view=view)

    def timer_callback(name_: str, state: str, secs_remain: int, timing_msg: Union[str, None]):
        embed.update_state(state)
        embed.update_time(secs_remain)
        try:
            bot.loop.create_task(ctx.edit_original_response(embed=embed))

            if state is DONE:  # If timer work is ended, button will be deleted
                bot.loop.create_task(ctx.edit_original_response(view=None))

            if timing_msg is not None:  # If timings exist, role will be noticed
                bot.loop.create_task(ctx.channel.send(f"{role.mention} {timing_msg}"))

        except Exception as e_:
            logger.error("Error in callback.", e=e_)

    reTimer.add_timer(Timer(name, secs, timer_callback, timings))


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
