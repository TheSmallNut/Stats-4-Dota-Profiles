from discord.ext import commands
import discord
import os
import API.scout as scout
import datetime


class stats(commands.Cog, name="Stats"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="scout", aliases=["Scout", "SCOUT"])
    @commands.has_permissions()
    async def _scout(self, ctx: commands.Context, teamLink):
        dotaIDS = scout.getDotaIDS(teamLink)
        teamLinks = []
        for playerID in dotaIDS:
            player = scout.playerProfile(playerID)
            dotabuffLink = scout.IDToDotabuff(playerID)
            embed = discord.Embed(
                title=f'{player["playerName"]}', url=f'{dotabuffLink}', color=0xfcba03)
            embed.set_author(
                name=player['playerName'], icon_url=player['icon_url'], url=player['steam'])
            file = discord.File(
                f"{os.getcwd()}/images/ranks/{player['rank']}.png", filename=f'{player["rank"]}.png')

            embed.set_thumbnail(url=f"attachment://{player['rank']}.png")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(file=file, embed=embed)


def setup(bot):
    print("Stats Cog Loaded")
    bot.add_cog(stats(bot))


def teardown(bot):
    print("Stats Cog Unloaded")
