#!/usr/bin/env python
import sys
import socket
import string
import time

#Setup
#HOST="irc.aberwiki.org"
HOST="localhost"
PORT=6667
NICK="echobot"
IDENT="athena"
REALNAME="athena"
CHAN="#mud"
readbuffer=""

socket=socket.socket()
print "connecting to host"
socket.connect((HOST, PORT))
time.sleep(1)
print "Setting nick"
socket.send("NICK %s\r\n" % NICK)
time.sleep(1)
socket.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
time.sleep(1)
print "Joining channel"
socket.send("JOIN :%s\r\n" % CHAN)
time.sleep(1)
print "Sending message to channel"
socket.send("PRIVMSG %s :%s\r\n" % (CHAN, "Hello there"))

#Funtionality
while 1:
	readbuffer=readbuffer+socket.recv(1024)
	temp=string.split(readbuffer, "\n")
	readbuffer=temp.pop()

	for line in temp:
		line=string.rstrip(line)
		line=string.split(line)
		print line
		who=line[0]
		what=line[1]
		if(line[1]=="PRIVMSG"):
			where=line[2]
			if(line[3]==":echo"):
				message=" ".join(line[4:])
				socket.send("PRIVMSG %s :%s\r\n" % (CHAN, message))

	try:
		f = open("athena.log", "a")
		f.write(line[0])
		f.close()
	except:
		pass
	if(line[0]=="PING"):
		socket.send("PONG %s\r\n" % line[1])
