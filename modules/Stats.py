from tkinter import CURRENT
from discord.ext import commands
import discord
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import API.scout as scout
import datetime
import validators
import asyncio
from multiprocessing import Process
from time import sleep


CURRENT_TOURNEY_IDS = [444, 443, 442, 441, 440]

allAD2LLeagues = scout.getAD2LTeams(CURRENT_TOURNEY_IDS)


def getLeagueLink(leagueInput):
    if validators.url(leagueInput):
        if 'https://dota.playon.gg/seasons/' in leagueInput:
            return leagueInput
        else:
            return None
    else:
        for league in allAD2LLeagues:
            if leagueInput.lower() in allAD2LLeagues[league]['Name'].lower():
                return allAD2LLeagues[league]['League_Link']


def getTeamLink(teamInput):
    if validators.url(teamInput):
        if 'https://dota.playon.gg/teams/' in teamInput:
            return teamInput
        else:
            return None
    else:
        for leagueID in allAD2LLeagues:
            for team in allAD2LLeagues[leagueID]['Teams']:
                if team['Name'].lower() == teamInput.lower():
                    return team['Team_Link']
    return None


def immortalRank(rank, leaderboard):
    if rank != 80 or leaderboard == None:
        return rank
    if leaderboard == 1:
        return 84
    elif leaderboard <= 10:
        return 83
    elif leaderboard <= 100:
        return 82
    elif leaderboard <= 1000:
        return 81
    else:
        return 80


def rankToFile(embed, rank, leaderboard):
    if leaderboard == None:
        file = discord.File(
            f"{os.getcwd()}/images/ranks/{rank}.png", filename=f'{rank}.png')
        embed.set_thumbnail(url=f"attachment://{rank}.png")
    else:
        rank = immortalRank(rank, leaderboard)
        img = Image.open(f"{os.getcwd()}/images/ranks/{rank}.png")
        I1 = ImageDraw.Draw(img)
        textSize = len(str(leaderboard))
        myFont = ImageFont.truetype('Arial.ttf', 40)
        I1.text((145 - (15 * textSize), 190),
                f"{leaderboard}", fill=(255, 255, 255), font=myFont)
        img.save(f"{os.getcwd()}/images/temp/temp.png")
        file = discord.File(
            f"{os.getcwd()}/images/temp/temp.png", filename=f'temp.png')
        embed.set_thumbnail(url=f"attachment://temp.png")

    return file


def playerEmbed(playerID):
    player = scout.playerProfile(playerID)
    dotabuffLink = scout.IDToDotabuff(playerID)
    embed = discord.Embed(
        title=f'{player["playerName"]}', url=f'{dotabuffLink}', color=0xfcba03)
    embed.set_author(
        name=player['playerName'], icon_url=player['icon_url'], url=player['steam'])
    embed.add_field(
        name='Links', value=f"[Dotabuff]({scout.IDToDotabuff(playerID, False)})\n[Esports]({dotabuffLink}) \n [Opendota](https://www.opendota.com/players/{playerID}) \n [Stratz](https://stratz.com/players/{playerID})", inline=True)
    file = rankToFile(embed, player['rank'], player['leaderboard'])
    #embed.timestamp = datetime.datetime.utcnow()
    return {'file': file, 'embed': embed}


def getAllStratzPages(dotaIDS):
    threads = []
    for user in dotaIDS:
        #t = Process(target=scout.getStratzPage, args=(user, 15, ))
        #threads.append(t)
        #t.start()
        scout.getStratzPage(user)
    #for thread in threads:
    #    thread.join()
        


async def longPlayerEmbed(playerID):
    # await scout.getStratzPage(playerID)
    files = []
    player = playerEmbed(playerID)
    files.append(player['file'])
    embed = player['embed']
    embed.set_image(url=f"attachment://{playerID}.png")
    file = discord.File(
        f"{os.getcwd()}/images/temp/{playerID}.png", filename=f'{playerID}.png')
    files.append(file)
    return {'files': files, 'embed': embed}


class stats(commands.Cog, name="Stats"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="scout", aliases=[])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.has_permissions()
    async def _scout(self, ctx: commands.Context, *, team):
        newTeamLink = getTeamLink(team)
        if newTeamLink == None:
            em = discord.Embed(
                title=f'"{team}" is not a valid team', color=0xff0000)
            await ctx.send(embed=em, delete_after=5)
            return
        await ctx.message.add_reaction('✅')
        em = discord.Embed(
            title=f'Getting Info on "{team}"', color=0x00ff00)
        await ctx.send(embed=em, delete_after=5)
        async with ctx.typing():
            dotaIDS = scout.getDotaIDS(newTeamLink)
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
        else:
            await ctx.send(f"An error occured: {error}")

    @commands.command(name='longScout', aliases=['ls'])
    @commands.cooldown(1, 20, commands.BucketType.guild)
    async def _longScout(self, ctx: commands.Context, *, team):
        newTeamLink = getTeamLink(team)
        if newTeamLink == None:
            em = discord.Embed(
                title=f'"{team}" is not a valid team', color=0xff0000)
            await ctx.send(embed=em, delete_after=5)
            return
        await ctx.message.add_reaction('✅')
        em = discord.Embed(
            title=f'Getting Info on "{team}"', color=0x00ff00)
        await ctx.send(embed=em, delete_after=5)
        async with ctx.typing():
            dotaIDS = scout.getDotaIDS(newTeamLink)
            teamLinks = []
            getAllStratzPages(dotaIDS)
            for playerID in dotaIDS:
                currentPlayerEmbed = await longPlayerEmbed(playerID)
                await ctx.send(files=currentPlayerEmbed['files'], embed=currentPlayerEmbed['embed'])
                os.remove(f"{os.getcwd()}/images/temp/{playerID}.png")

    @commands.command(name="league", aliases=[])
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def _league(self, ctx: commands.Context, league):
        async with ctx.typing():
            newLeagueLink = getLeagueLink(league)
            leagueData = scout.getLeagueData(newLeagueLink)
            leagueStandings = leagueData['standings']
            leagueStats = leagueData['stats']
            embed = discord.Embed(
                title=f'{leagueStats["League_Name"]}', color=0x00ff00
            )
            for team in leagueStandings:
                embed.add_field(name=f"{scout.ordinal(int(team['Place']))}",
                                value=f"[{team['Name']}]({team['Team_Link']}) - {team['Wins']}", inline=False)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

    # @_league.error
    # async def _league_error(self, ctx, error):
    #    if isinstance(error, commands.CommandOnCooldown):
    #        embed = discord.Embed(title=f"Slow it down!",
    #                              description=f"Try again in {error.retry_after:.2f}s.", color=0xff0000)
    #        await ctx.send(embed=embed)
    #    else:
    #        e = discord.Embed(
    #            title=f"An error occured: {error}", color=0xff0000)
    #        print(error)
    #        await ctx.send(embed=e)

    @commands.command(name='teams')
    @commands.cooldown(1, 20, commands.BucketType.guild)
    async def _teams(self, ctx: commands.Context):
        em = discord.Embed(title='Current Teams in AD2L', color=0x00ff00)
        for leagueID in allAD2LLeagues:
            league = allAD2LLeagues[leagueID]
            teamsInLeague = ""
            for team in league['Teams']:
                teamsInLeague += f"**{scout.ordinal(int(team['Place']))}** - {team['Name']}\n"
            em.add_field(name=f'{league["Name"]}',
                         value=teamsInLeague, inline=False)
        await ctx.send(embed=em)


def setup(bot):
    print("Stats Cog Loaded")
    bot.add_cog(stats(bot))


def teardown(bot):
    print("Stats Cog Unloaded")
