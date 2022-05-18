import requests
from bs4 import BeautifulSoup
from lxml import etree
import validators
import discord
import json



#gets AD2L Teams and stores them in a JSON like object, the json looks like this:
#{
#   "Tourney_ID": {
#       "Name": "Tourney_Name",
#       "Teams": [
#           {
#               "Name": "Team_Name",
#               "Wins": "Wins",
#               "Place": "Place",
#               "Team_Link": "Team_Link",
#               "Division_Link": "Division_Link",
#               "Division_Number": "Division_Number"
#           },
#           ...
#       ],
#       "ID": "Tourney_ID",
#       "League_Link": "League_Link"
#   },
#   ...
#}
def getAD2LTeams(tourneyIDS):
    tourneys = {}
    for tourneyID in tourneyIDS:
        tourneyURL = f'https://dota.playon.gg/seasons/{str(tourneyID)}'
        website = requests.get(tourneyURL)
        soupPage = BeautifulSoup(website.content, 'html.parser')
        convertedPage = etree.HTML(str(soupPage))
        # have to convert to allow me to check xpath for some reason
        tourneyName = convertedPage.xpath(
            '/html/body/div[2]/div[1]/h2')[0].text
        tourneys[str(tourneyID)] = {
            'Name': tourneyName.split(" ")[1],
            'Teams': [],
            'ID': str(tourneyID),
            'League_Link': tourneyURL
        }
        teamsInLeague = soupPage.find(
            class_="table table-hover table-bordered").find('tbody')
        for team in teamsInLeague('tr'):
            teamData = team.find_all('td')
            JSON = {
                "Name": teamData[1].getText(),
                "Wins": teamData[2].getText(),
                "Place": teamData[0].getText(),
                "Team_Link": f"https://dota.playon.gg{teamData[1].find('a')['href']}",
                'Division_Link': tourneyURL,
                'Division_Number': tourneyURL.split('/')[-1]
            }
            tourneys[str(tourneyID)]['Teams'].append(JSON)
    print("AD2L Teams Loaded")
    return tourneys


#####################################################
#                                                   #                        
#    ██████╗ █████╗  █████╗ ██╗   ██╗████████╗      #
#   ██╔════╝██╔══██╗██╔══██╗██║   ██║╚══██╔══╝      #
#   ╚█████╗░██║  ╚═╝██║  ██║██║   ██║   ██║         # 
#    ╚═══██╗██║  ██╗██║  ██║██║   ██║   ██║         #
#   ██████╔╝╚█████╔╝╚█████╔╝╚██████╔╝   ██║         #
#   ╚═════╝  ╚════╝  ╚════╝  ╚═════╝    ╚═╝         #
#                                                   #
#####################################################


# Gets the link from the input and checks if it already is a link or not
def getScoutLink(teamInput, AD2LTEAMS):
    if validators.url(teamInput):
        if 'https://dota.playon.gg/teams/' in teamInput:
            return teamInput
        else:
            return None
    else:
        for leagueID in AD2LTEAMS:
            for team in AD2LTEAMS[leagueID]['Teams']:
                if (team['Name'].lower() == teamInput.lower()) or (len(teamInput) > 3 and teamInput.lower() in team['Name'].lower()):
                    return team['Team_Link'].strip()
    return None


# Gets whole team's dota 2 IDS
def getDotaIDS(teamLink):
    URL = f'{teamLink}'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all(class_="DotabuffIcon")
    DotaIDS = []
    for player in results:
        DotaIDS.append(int(player.get('href').split("/")[-1]))
    return DotaIDS


# Gets one player's stats from opendota
def scoutPlayerJSON(account_id):
    url = f'https://api.opendota.com/api/players/{account_id}'
    playerData = requests.get(url).json()
    playerName = playerData['profile']['personaname']
    thumbnail = playerData['profile']['avatarfull']
    icon_url = playerData['profile']['avatar']
    rank = playerData['rank_tier']
    steam = playerData['profile']['profileurl']
    leaderboard = None
    if int(rank) == 80:
        leaderboard = playerData['leaderboard_rank']
    return {
        'playerName': playerName,
        'thumbnail': thumbnail,
        'rank': rank,
        'leaderboard': leaderboard,
        'steam': steam,
        'icon_url': icon_url,
        'account_id': account_id
    }



#############################################################################################
#                                                                                           #
#   ██╗     ███████╗ █████╗  ██████╗ ██╗   ██╗███████╗  ██████╗  █████╗ ████████╗ █████╗    #
#   ██║     ██╔════╝██╔══██╗██╔════╝ ██║   ██║██╔════╝  ██╔══██╗██╔══██╗╚═ ██╔   ██╔══██╗   #
#   ██║     █████╗  ███████║██║  ██╗ ██║   ██║█████╗    ██║  ██║███████║   ██║   ███████║   #
#   ██║     ██╔══╝  ██╔══██║██║   ██╗██║   ██║██╔══╝    ██║  ██║██╔══██║   ██║   ██╔══██║   #
#   ███████╗███████╗██║  ██║╚██████╔╝╚██████╔╝███████╗  ██████╔╝██║  ██║   ██║   ██║  ██║   #
#   ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝  ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝   #
#                                                                                           #
#############################################################################################



    # Gets the link for the league from the league name and checks if it already is a link or not
def getLeagueLink(leagueInput, ad2lLeagues):
    if validators.url(leagueInput):
        if 'https://dota.playon.gg/seasons/' in leagueInput:
            return leagueInput
        else:
            return None
    else:
        for league in ad2lLeagues:
            if leagueInput.lower() in ad2lLeagues[league]['Name'].lower():
                return ad2lLeagues[league]['League_Link']


# League Data Returns a dictionary with the following keys:
#   'stats': {
#       'League_Name': 'League_Name',
#       'Number_Of_Teams': 'Number_Of_Teams'
#   }
#   'standings': [
#   {
#        'Team_Name': 'Team_Name',
#        'Wins': 'Wins', 
#        'Place': 'Place',
#        'Team_Link': 'Team_Link']
#   },
#   ...
#   ]


def leagueData(leagueURL):
    soup = BeautifulSoup(requests.get(leagueURL).content, "html.parser")
    standings = leagueStandings(soup)
    stats = leagueStats(soup)
    return {
        'stats': stats,
        'standings': standings
    }

def leagueStandings(leagueWebsiteData):
    results = leagueWebsiteData.find(class_="table table-hover table-bordered")
    teamsListHTML = results.find('tbody')
    teamsList = []
    for team in teamsListHTML('tr'):
        teamData = team.find_all('td')
        teamsList.append({
            "Name": teamData[1].getText(),
            "Wins": teamData[2].getText(),
            "Place": teamData[0].getText(),
            "Team_Link": "https://dota.playon.gg" + teamData[1].find('a')['href']
        })
    return teamsList

def leagueStats(leagueWebsiteData):
    name = leagueWebsiteData.find(id='main').find(
        class_='text-center')('h2')[0].getText()
    teams = len(leagueWebsiteData.find(
        class_="table table-hover table-bordered").find('tbody')('tr'))
    toReturn = {
        'League_Name': name,
        'Number_Of_Teams': teams
    }
    return toReturn