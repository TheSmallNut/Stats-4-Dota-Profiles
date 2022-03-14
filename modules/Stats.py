from discord.ext import commands
import discord
import os
import API.scout as scout
import datetime


def playerEmbed(playerID):
    player = scout.playerProfile(playerID)
    dotabuffLink = scout.IDToDotabuff(playerID)
    print(player["rank"])
    embed = discord.Embed(
        title=f'{player["playerName"]}', url=f'{dotabuffLink}', color=0xfcba03)
    embed.set_author(
        name=player['playerName'], icon_url=player['icon_url'], url=player['steam'])
    embed.add_field(
        name='Links', value=f"[Dotabuff]({scout.IDToDotabuff(playerID, False)})\n[Esports]({dotabuffLink}) \n [Opendota](https://www.opendota.com/players/{playerID}) \n [Stratz](https://stratz.com/players/{playerID})", inline=True)
    file = discord.File(
        f"{os.getcwd()}/images/ranks/{player['rank']}.png", filename=f'{player["rank"]}.png')

    embed.set_thumbnail(url=f"attachment://{player['rank']}.png")
    #embed.timestamp = datetime.datetime.utcnow()
    return {'file': file, 'embed': embed}


class stats(commands.Cog, name="Stats"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="scout", aliases=[])
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.has_permissions()
    async def _scout(self, ctx: commands.Context, teamLink):
        dotaIDS = scout.getDotaIDS(teamLink)
        teamLinks = []
        for playerID in dotaIDS:
            currentPlayerEmbed = playerEmbed(playerID)
            await ctx.send(file=currentPlayerEmbed['file'], embed=currentPlayerEmbed['embed'])

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
