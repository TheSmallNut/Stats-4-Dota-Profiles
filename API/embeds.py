import datetime
import discord
import os

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont



def ordinal(n): return "%d%s" % (
    n, "tsnrhtdd"[(n//10 % 10 != 1)*(n % 10 < 4)*n % 10::4])


def message(message, color=0x00ff00):
    if str(color).lower() == "red":
        color = 0xff0000
    elif str(color).lower() == "yellow":
        color = 0xffff00
    embed = discord.Embed(
                title=f'{message}', color=color
            )
    embed.timestamp = datetime.datetime.utcnow()
    return embed

def leagueEmbed(data):
    leagueStandings = data['standings']
    leagueStats = data['stats']
    embed = discord.Embed(
                title=f'{leagueStats["League_Name"]}', color=0x00ff00
            )
    for team in leagueStandings:
        embed.add_field(name=f"{ordinal(int(team['Place']))}",
            value=f"[{team['Name']}]({team['Team_Link']}) - {team['Wins']}", inline=False)
    embed.timestamp = datetime.datetime.utcnow()
    return embed


def teamsEmbed(AD2LLEAGUES):
    embed = discord.Embed(title='Current Teams in AD2L', color=0x00ff00)
    for leagueID in AD2LLEAGUES:
        league = AD2LLEAGUES[leagueID]
        teamsInLeague = ""
        for team in league['Teams']:
            teamsInLeague += f"**{ordinal(int(team['Place']))}** - {team['Name']}\n"
        embed.add_field(name=f'{league["Name"]}', value=teamsInLeague, inline=False)
    return embed


def checkForImmortal(rank, leaderboard):
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


def playerEmbedAndFile(player):
    embed = discord.Embed(title=f'{player["playerName"]}', url=f'https://www.dotabuff.com/players/{player["account_id"]}', color=0xfcba03)
    embed.set_author(name=player['playerName'], icon_url=player['icon_url'], url=player['steam'])
    embed.add_field(name='Links', value=f"[Dotabuff](https://www.dotabuff.com/players/{player['account_id']}) \n [Esports](https://www.dotabuff.com/esports/players/{player['account_id']}) \n [Opendota](https://www.opendota.com/players/{player['account_id']}) \n [Stratz](https://stratz.com/players/{player['account_id']})", inline=True)
    file = rankToFile(player["rank"], embed, player["leaderboard"])
    return {'file': file, 'embed': embed}

def rankToFile(rank, embed, leaderboard):
    rank = checkForImmortal(rank, leaderboard)
    if rank != 80:
        file = discord.File(f"{os.getcwd()}/images/ranks/{rank}.png", filename=f'{rank}.png')
        embed.set_thumbnail(url=f'attachment://{rank}.png')
    else:
        img = Image.open(f"{os.getcwd()}/images/ranks/{rank}.png")
        I1 = ImageDraw.Draw(img)
        textSize = len(str(leaderboard))
        myFont = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 40)
        I1.text((145 - (15 * textSize), 190),
                f"{leaderboard}", fill=(255, 255, 255), font=myFont)
        img.save(f"{os.getcwd()}/images/temp/temp.png")
        file = discord.File(
            f"{os.getcwd()}/images/temp/temp.png", filename=f'temp.png')
        embed.set_thumbnail(url=f"attachment://temp.png")
    return file


