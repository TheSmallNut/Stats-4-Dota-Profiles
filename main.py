from discord.ext import commands
import API.secret as secret
import os
from discord import Intents
import discord
from discord_slash import SlashCommand

intents = Intents.default()
intents.members = True
activity = discord.Game(name="AD2L Stats | !help")
bot = commands.Bot(command_prefix='!', activity=activity,
                   intents=intents, case_insensitive=True)
slash = SlashCommand(bot, sync_commands=True)


def loadModules():
    # Change "cogs" to your folder name
    for filename in os.listdir("./modules"):
        if filename.endswith(".py"):
            if 'copy' not in filename:
                bot.load_extension(f"modules.{filename[:-3]}")


if __name__ == '__main__':
    # bot.remove_command('help')
    loadModules()
    bot.remove_command("longScout")
    bot.run(secret.DOTA_2_SCOUTING_BOT)
