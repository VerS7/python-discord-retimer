"""
File with description strings
"""


# ReTime command
RETIME_DESCRIPTION = "Creates timer with notification."
RETIME_ARG_NAME = "Name of timer."
RETIME_ARG_TIME = "%d:%h:%m | Example: 7d:5h:11m / 14h:30m / 1h / 30m / " \
                  "You can also use something like 30h, 100m, etc..."
RETIME_ARG_ROLE = "Role to be noticed | Example: @everyone"
RETIME_ARG_TIMINGS = "Timings before end when notification appears with @ message | " \
                     "Example: 1h-Hurry up! / 1h:30m-Almost ready!, 30m-Too Close... / " \
                     "3d:15h-Deadline is approaching, 2d-Hurry!, 12h:30m-Last chance..."
RETIME_ARG_DESCRIPTION = "Your timer description."

# Retimers command
RETIMERS_DESCRIPTION = "Show all enqueued timers."

# Discord embed timer messages
TIMER_DONE_MSG = "Time is up."
TIMER_TICKING_MSG = "Ticking..."
TIMER_PAUSE_MSG = "On pause."

# Discord embed descriptions
RETIMER_EMBED_TITLE = "ReTimer"
RETIMER_EMBED_DESCRIPTION = "Timing the timings!"
