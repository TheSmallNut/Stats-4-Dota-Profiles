from discord.ext import commands
import API.secret as secret
import os
from discord import Intents

intents = Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)


def loadModules():
    # Change "cogs" to your folder name
    for filename in os.listdir("./modules"):
        if filename.endswith(".py"):
            if 'copy' not in filename:
                bot.load_extension(f"modules.{filename[:-3]}")


loadModules()


bot.run(secret.DOTA_2_SCOUTING_BOT)
