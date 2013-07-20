from mud_bot import mud_bot

#set up the bot instance so that athena commands can register with it
bot = mud_bot()

import athena.commands

def main():
    bot.start()


if __name__ == "__main__":
    main()
