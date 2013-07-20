import sys
import socket
import select

from event_hook import event_hook

class irc_client:
    """Send and receive messages from an IRC server.

    Subscribe to the events you want, then call connect()"""
    def __init__(self, host, port, id, real_name, nick):
        """
        init

        host: IRC server domain name/IP address
        port: IRC server port number
        id: IRC identity
        real_name: IRC real name
        nick: IRC nick
        """
        self._host = host
        self._port = port
        self._id = id
        self._real_name = real_name
        self._nick = nick
        self._input_buffer = ""
        # Data that is ready to immediately be written to the host
        self._output_buffer = ""

        self._sock = socket.socket()

        # Listener params:
        # Server - the server which sent the ping request, with a : in front
        self.ping_event = event_hook()
        # Listener params:
        # Nick - nick of the user who sent the PM
        # Message - message received
        self.pm_event = event_hook()
        # Listener params:
        # Nick - nick of the user who sent the PM
        # Message - message received
        # Channel - channel that the message was received in
        self.msg_event = event_hook()

    def send_pong(self, server):
        """Send PONG"""
        self._output_buffer += "PONG %s\r\n" % server

    def send_nick(self):
        """Send NICK"""
        self._output_buffer += "NICK %s\r\n" % self._nick

    def send_user(self):
        """Send USER"""
        self._output_buffer += "USER %s %s bla :%s\r\n" % (self._id, self._host, self._real_name)

    def send_join(self, channel):
        """Send JOIN channel"""
        self._output_buffer += "JOIN :%s\r\n" % channel

    def send_msg_channel(self, channel, msg):
        """Send PRIVMSG to channel"""
        self._output_buffer += "PRIVMSG %s :%s\r\n" % (channel, msg)

    def send_msg_user(self, user, msg):
        """Send PRIVMSG to user"""
        self._output_buffer += "PRIVMSG %s :%s\r\n" % (user, msg)

    def connect(self):
        """Connect to the IRC server"""
        self._sock.connect((self._host, self._port))

    def close(self):
        """Close the IRC connection"""
        self._sock.close()

    def read_and_process(self):
        """Read and process data from the IRC connection"""
        ready_to_read, _ready_to_write, _in_error = None, None, None
        try:
            ready_to_read, _ready_to_write, _in_error = select.select([self._sock], [self._sock], [], 10)
            # Only read if there is data to read (to avoid blocking)
            if ready_to_read:
                new_data = self._sock.recv(4096)
                if new_data:
                    self._input_buffer += new_data
                else:
                    raise Exception("Connection closed by host")
        except:
            if self._sock:
                self._sock.close()
            raise

        self._process_input_buffer()

    def _process_input_buffer(self):
        """Process the input buffer"""
        newline_pos = self._input_buffer.find("\n")

        while newline_pos > -1:
            input_line = self._input_buffer[:newline_pos]
            self._input_buffer = self._input_buffer[newline_pos + 1:]
            if input_line:
                # Lines may or may not end in \r: remove it
                if input_line[-1] == "\r":
                    input_line = input_line[:-1]
                self.process_input_line(input_line)

            newline_pos = self._input_buffer.find("\n")

    def process_input_line(self, line):
        """Process an IRC line (e.g. from the host) excluding the \n or \r\n"""
        print "Host: [%s]" % line
        if line[0] == ":":
            words = line[1:].split(" ", 3)
            if len(words) == 4 and words[1] == "PRIVMSG":
                user_nick = words[0]
                exclamation_pos = user_nick.find("!")
                if exclamation_pos > -1:
                    user_nick = user_nick[:exclamation_pos]
                # Ignore the colon at the start of the message
                msg = words[3][1:]
                if words[2] == self._nick:
                    self.pm_event.fire(user_nick, msg)
                else:
                    self.msg_event.fire(user_nick, msg, words[2])
        else:
            words = line.split()
            if len(words) >= 2 and words[0] == "PING":
                self.ping_event.fire(words[1])

    def write_to_host(self):
        """Write the contents of the output buffer to the host"""
        total_sent = 0
        try:
            while total_sent < len(self._output_buffer):
                # Not using select.select for writing, as the host should always be ready to receive data
                sent_len = self._sock.send(self._output_buffer[total_sent:])
                total_sent += sent_len
                if sent_len == 0:
                    raise Exception("Only succeeded to send [%d/%d] characters to the host. Output buffer: [%s]"
                            % (total_sent, len(self._output_buffer), self._output_buffer))
            # Clear the output buffer as it has all been sent to the host
            if self._output_buffer:
                print "Bot: [%s]" % self._output_buffer.strip()
            self._output_buffer = ""
        except:
            if self._sock:
                self._sock.close()
            raise


