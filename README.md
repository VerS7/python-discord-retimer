# ReTimer Discord Bot
![logo](https://github.com/VerS7/python-discord-retimer/blob/master/assets/logo.png)

### Version: 1.0.0

# Simple Discord bot with timer functionality

# Info

**Simple timers in your Discord server!**

**!WARNING!** timers work only while your application running. If you restart your application, all timers will disappear!

# Using

This bot have few simple commands.

### /retime command

`/retime <name> <about> <time> <role> <timings>`

`<name>` - Name of your timer. Must be unique, don't use any name from your active timers

`<about>` - Description of your timer. Anything to be shown

`<time>` - How much time your timer will tick. Must be formatted like **%d:%h:%m** for example: **7d:5h:11m / 14h:30m / 1h / 30m**

`<role>` - Noticing role. Any role like **@everyone**, etc...

`<timings>` - Timings when timer will notice with message. For example: **1d-Deadline is approaching, 12h-Hurry!, 30m-Last chance...** 

Full command must look like this:  
>/retime _name_: **Break reminder  
> _about_: **Don't forget to take a break!**  
> _time_: **8h**  
> _role_: **@Workers**  
> _timings_: **7h-First break, 6h-Second break, 5h-Long break. Time to eat!, 
> 3h-Smoke break, 1h-Last break. Working day is almost done!**

If command is correct, you will see this:  
![retimer_example](https://github.com/VerS7/python-discord-retimer/blob/master/assets/retime_example.png)

### /retimers command

`/retimers`

Show all active timers. Nothing else!

# Running

## Manual
For manual running you need:
1. Clone this repository or **Code -> Download ZIP** and unzip to any folder 
2. Create your **Discord** bot application. [Discord Developer Portal](https://discord.com/developers/applications/)
3. Install **Python 3.10** or newer version
4. Go to **src/config.py** and fill **TOKEN** with your **Discord Application Token** and optionally **GUILD_ID**
5. Install requirements **pip install -r requirements.txt**
6. Start **main.py**

After this you can add your **Discord Application** to server.

**ReTimer** bot will be online. Now you can use commands. See **Using**

## Docker
For running via **Docker** you need:

_In progress..._
