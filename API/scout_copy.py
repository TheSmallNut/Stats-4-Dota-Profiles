import requests
from bs4 import BeautifulSoup


def getTeamInfo(teamLink):
    website = requests.get(teamLink)
    # Soup Webiste
    soupWebsite = BeautifulSoup(website.content, "html.parser")
    # Gets team statistics (Captain, Team Name, Logo, Etc)
    teamStats = getTeamStats(soupWebsite)
    # Makes the team Embed for discord
    teamEmbed = makeTeamEmbed(teamStats)
    # Scrapes and gets all players on a team and returns their ID's
    players = getPlayersByID(soupWebsite)
    embeds = {
        'teamEmbed': teamEmbed,
        'playersEmbeds': []
    }

    # MIGHT NEED TO REFACTOR EMBED TO ALLOW FOR ROLE SEARCHING AND RETURNING
    # going through each player and getting their stats from different websites (dotabuff, Open Dota API)
    for player in players:
        # Gets stats for the player
        playerStats = getPlayerStats(player)
        # Turns the stats into an embed for discord
        playerEmbed = makePlayerEmbed(playerStats)
        # Adds it to embeds to get returned later
        embeds['playersEmbeds'].append(playerEmbed)

    return embeds

# gets team stats through AD2L and then later through Dotabuff most likely? Still unsure of where


def getTeamStats(websiteInfo):
    None

# Takes team stats and returns a Discord Embed to send later


def makeTeamEmbed(teamStats):
    None

# gets all players from AD2L Website


def getPlayerIDs(websiteInfo):
    playerList = websiteInfo.find(
        class_="rosterholder").find('ul').find_all('li')
    playerIDS = []
    # loops through all players and grabs the end of the href which is the ID of the player
    for player in playerList:
        playerIDS.append(
            int(player.find_all('a')[0].get('href').split("/")[-1]))
    return playerIDS

# Gets player stats from websites
# Stats I want: Username, Rank, Profile Photo, Leaderboard Status,


def getPlayerStats(player):
    None

# Takes the player stats and returns a Discord Embed to send later


def makePlayerEmbed(playerStats):
    None
