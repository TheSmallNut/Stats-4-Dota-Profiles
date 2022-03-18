from discord.ext import commands
import discord
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import API.scout_copy as scout
import datetime


class stats(commands.Cog, name="Stats"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="scout", aliases=[])
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.has_permissions()
    async def _scout(self, ctx: commands.Context, teamLink):
        em = discord.Embed(
            title=f'Getting Info', color=0x00ff00)
        await ctx.send(embed=em, delete_after=5)
        scout.getTeamInfo(teamLink)

    @_scout.error
    async def _scout_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f"Slow it down!",
                                  description=f"Try again in {error.retry_after:.2f}s.", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command(name="league", aliases=[])
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def _league(self, ctx: commands.Context, leagueLink):
        leagueData = scout.getLeagueData(leagueLink)
        leagueStandings = leagueData['standings']
        leagueStats = leagueData['stats']
        embed = discord.Embed(
            title=f'{leagueStats["League_Name"]}', color=0xffffff
        )
        for team in leagueStandings:
            embed.add_field(name=f"{scout.ordinal(int(team['Place']))}",
                            value=f"[{team['Name']}]({team['Team_Link']}) - {team['Wins']}", inline=False)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @_league.error
    async def _league_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f"Slow it down!",
                                  description=f"Try again in {error.retry_after:.2f}s.", color=0xff0000)
            await ctx.send(embed=embed)


def setup(bot):
    print("Stats Cog Loaded")
    bot.add_cog(stats(bot))


def teardown(bot):
    print("Stats Cog Unloaded")
