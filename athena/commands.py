"""This module defines athena's base commands.

"""

import sys
from athena import bot

@bot.register_command("echo")
def echo( *args, **kwargs ):
    return "%s: %s" % (kwargs['sender']," ".join(args[1:]))

@bot.register_command("reload")
def reload_commands(*args, **kwargs):
    reload(sys.modules[__name__])
    return "%s: Reloaded command module" % kwargs['sender']
