from discord.ext import commands
import API.secret as secret
import os
from discord import Intents
import discord

intents = Intents.default()
intents.members = True
activity = discord.Game(name="AD2L Stats | !help")
bot = commands.Bot(command_prefix='!', activity=activity,
                   intents=intents, case_insensitive=True)


def loadModules():
    # Change "cogs" to your folder name
    for filename in os.listdir("./modules"):
        if filename.endswith(".py"):
            if 'copy' not in filename:
                bot.load_extension(f"modules.{filename[:-3]}")


if __name__ == '__main__':
    loadModules()
    bot.run(secret.DOTA_2_SCOUTING_BOT)
