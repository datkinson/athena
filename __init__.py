from mud_bot import mud_bot

bot = mud_bot()

@bot.register_command("echo")
def echo( *args, **kwargs ):
    return "%s: %s" % (kwargs['sender']," ".join(args[1:]))

def main():
    bot.start()


if __name__ == "__main__":
    main()
