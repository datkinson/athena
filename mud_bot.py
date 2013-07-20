import traceback
import time

from irc_client import irc_client


class mud_bot:
    """An IRC MUD"""
    def __init__(self):
        self._client = None
        self._command_prefix = "!"
        self._main_channel = "#mud"
        self._nick = "athenabot"
        self._registered_commands = {}

    def register_command(self, name):
        """Decorator function that allows registration of 'commands' """
        def decorator( func ):
            self._registered_commands[name] = func
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            
            return wrapper
        return decorator


    def start(self):
        """Start the MUD"""
        max_attempts = 1
        for attempt_num in xrange(max_attempts):
            try:
                print "Starting MUD"
                print ""
                #self._client = irc_client("nopro.be", 6697, "athenazan", "athena", "echorot", "#mud")
                self._client = irc_client("irc.aberwiki.org", 6667, "athena", "athena", self._nick)

                self._client.ping_event += self._on_ping
                self._client.pm_event += self._on_pm
                self._client.msg_event += self._on_msg

                self._client.connect()
                self._client.send_nick()
                self._client.send_user()
                self._client.send_join(self._main_channel)
                self._client.send_msg_channel(self._main_channel, "Type %shelp for info" % self._command_prefix)

                while True:
                    self._client.read_and_process()
                    self._client.write_to_host()
                    time.sleep(1)

            except:
                print "Error: " + traceback.format_exc()
                if self._client:
                    self._client.close()

            if attempt_num < max_attempts - 1:
                print ""
                print "Reconnecting bot in 10 seconds"
                print ""
                time.sleep(10)

        print "Bot stopped"

    def _on_ping(self, server):
        self._client.send_pong(server)

    def _on_pm(self, nick, msg):
        self._client.send_msg_channel(self._main_channel, nick + " messaged me: " + msg)

    def _on_msg(self, nick, msg, channel):
        if channel == self._main_channel:
            if len(msg) > len(self._command_prefix) and msg.startswith(self._command_prefix):
                
                cmdstring = msg[len(self._command_prefix):]
                cmd_array = cmdstring.split(" ")
                command = cmd_array[0]

                if command == "help":
                    self._client.send_msg_user(nick, "Type %shelp for help. It's helpful." % self._command_prefix)
                elif command in self._registered_commands:
                    self._client.send_msg_channel(self._main_channel, self._registered_commands[command](*cmd_array, sender=nick))

