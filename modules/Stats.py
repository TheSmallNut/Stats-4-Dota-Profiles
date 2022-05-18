from discord.ext import commands
import discord
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
import API.scouting as scouting
import API.embeds as embeds

GUILDS = []
TOURNEY_IDS = [458, 457, 456, 455, 454, 453]
ERROR_LOGGING_CHANNEL = 976043428393668608


# Will be ran whenever the bot is run and it will get all the teams from AD2L
AD2LLEAGUES = scouting.getAD2LTeams(TOURNEY_IDS)




class stats(commands.Cog, name="Stats"):
    def __init__(self, bot):
        self.bot = bot
        
    @cog_ext.cog_slash(description="Sends teams in a certain league with links to their AD2L page", options = [
        create_option(
            name = "league", 
            description = "The league you want to get teams from | Can be sent as a URL from AD2L or the League Name", 
            required = True, 
            option_type = 3
            )])
    async def league(self, ctx: SlashContext, league: str):
        try:
            await ctx.send(embed = embeds.message(f"Getting teams from {league}", color = "yellow"))
            leagueURL = scouting.getLeagueLink(league, AD2LLEAGUES)
            if leagueURL == None:
                await ctx.send(embed = embeds.message(f"Could not find league {league}", color = 0xff0000))
                return
            print(leagueURL)
            data = scouting.leagueData(leagueURL)
            embed = embeds.leagueEmbed(data)
            await ctx.send(embed=embed)
        except Exception as e:
            channel = self.bot.get_channel(976043428393668608)
            embed = embeds.message(f"ERROR: {str(repr(e))} \nCommand: {ctx.name}\nARGS: {ctx.args}", "red")
            await channel.send(embed=embed)
    
    @cog_ext.cog_slash(description="Sends all teams in every league without links", options=[])
    async def teams(self, ctx: SlashContext):
        try:
            await ctx.send(embed = embeds.message("Getting teams", color = "yellow"))
            await ctx.send(embed=embeds.teamsEmbed(AD2LLEAGUES))
        except Exception as e:
            channel = self.bot.get_channel(976043428393668608)
            embed = embeds.message(f"ERROR: {str(repr(e))} \nCommand: {ctx.name}\nARGS: {ctx.args}", "red")
            await channel.send(embed=embed)
    
    @cog_ext.cog_slash(description="Scouts one team and returns current ranks", options=[
        create_option(
            name = "team",
            description = "The team you want to scout | Can be sent as a link from AD2L or the Name",
            required = True,
            option_type = 3
            )])
    async def scout(self, ctx: SlashContext, team: str):
        try:
            await ctx.send(embed = embeds.message(f"Scouting {team}", color = "yellow"))
            teamURL = scouting.getScoutLink(team, AD2LLEAGUES)
            if teamURL == None:
                await ctx.send(embed = embeds.message(f"Could not find team {team}", color = 0xff0000))
                return
            for playerID in scouting.getDotaIDS(teamURL):
                playerStats = scouting.scoutPlayerJSON(playerID)
                playerEmbedAndFile = embeds.playerEmbedAndFile(playerStats)
                await ctx.send(file=playerEmbedAndFile['file'], embed=playerEmbedAndFile['embed'])
        except Exception as e:
            channel = self.bot.get_channel(976043428393668608)
            embed = embeds.message(f"ERROR: {str(repr(e))} \nCommand: {ctx.name}\nARGS: {ctx.args}", "red")
            await channel.send(embed=embed)

    @cog_ext.cog_slash(description="Refreshes all AD2L Teams that are already there", options=[])
    async def refresh(self, ctx: SlashContext):
        try:
            await ctx.send(embed = embeds.message("Attempting to refresh now!", "yellow"))
            global AD2LLEAGUES
            AD2LLEAGUES = scouting.getAD2LTeams(TOURNEY_IDS)
            await ctx.send(embed = embeds.message("Cache Refreshed, new teams should now be added to the roster"))
        except Exception as e:
            try:
                embed = embeds.message("ERROR Refreshing Cache, please contact TheSmallNut", "red")
                await ctx.send(embed = embed)
            except Exception as E:
                channel = self.bot.get_channel(976043428393668608)
                await channel.send(embed=embeds.message(f"ERROR: {str(repr(e))} \nCommand: {ctx.name}\nARGS: {ctx.args}", "red"))
            channel = self.bot.get_channel(976043428393668608)
            await channel.send(embed=embeds.message(f"ERROR: {str(repr(e))} \nCommand: {ctx.name}\nARGS: {ctx.args}", "red"))



    @commands.Cog.listener()
    async def on_ready(self):
        GUILDS = []
        GUILD_NAMES = []
        for guild in self.bot.guilds:
            GUILDS.append(guild.id)
            GUILD_NAMES.append(guild.name)
        print(GUILD_NAMES)
    

def setup(bot):
    print("Stats Cog Loaded")
    bot.add_cog(stats(bot))


def teardown(bot):
    print("Stats Cog Unloaded")