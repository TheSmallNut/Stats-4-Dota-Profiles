#!/usr/bin/python3
from discord.ext import commands
import API.secret as secret
import os
from discord import Intents
import discord
from discord_slash import SlashCommand


intents = Intents.default()
intents.members = True
activity = discord.Game(name="AD2L Stats")
bot = commands.Bot(command_prefix='!', activity=activity,
                   intents=intents, case_insensitive=True)
slash = SlashCommand(bot, sync_commands=True)


def loadModules():
    # Change "cogs" to your folder name
    for filename in os.listdir("./modules"):
        if filename.endswith(".py"):
            bot.load_extension(f"modules.{filename[:-3]}")


if __name__ == '__main__':
    # bot.remove_command('help')
    loadModules()
    bot.run(secret.TEST)
