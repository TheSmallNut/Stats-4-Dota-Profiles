import requests
from bs4 import BeautifulSoup
import json


def ordinal(n): return "%d%s" % (
    n, "tsnrhtdd"[(n//10 % 10 != 1)*(n % 10 < 4)*n % 10::4])


def getDotaIDS(teamLink):
    URL = f'{teamLink}'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all(class_="DotabuffIcon")
    DotaIDS = []
    for player in results:
        DotaIDS.append(int(player.get('href').split("/")[-1]))
    return DotaIDS


def getLeagueData(leagueLink):
    page = requests.get(leagueLink)
    soup = BeautifulSoup(page.content, "html.parser")
    standings = leagueStandings(soup)
    stats = leagueStats(soup)
    return {
        'stats': stats,
        'standings': standings
    }


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


def IDToDotabuff(id, esports=True):
    if esports:
        return f'https://www.dotabuff.com/esports/players/{id}'
    else:
        return f'https://www.dotabuff.com/players/{id}'


def playerProfile(account_id):
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
        'icon_url': icon_url
    }


def getAD2LTeams():
    page = requests.get('https://dota.playon.gg/seasons')
    soup = BeautifulSoup(page.content, 'html.parser')
    eachTourney = soup.find(class_='dropdown-menu tourneyDropdown')
    tourneys = {}
    for tourney in eachTourney.find_all('li'):
        endURL = tourney.find('a')['href']
        tourneyURL = f'https://dota.playon.gg{endURL}'
        tourneyID = endURL.split("/")[-1]
        tourneyName = tourney.getText().strip()
        tourneys[str(tourneyID)] = {
            'Name': tourneyName,
            'Teams': [],
            'ID': str(tourneyID)
        }
        website = requests.get(tourneyURL)
        soupPage = BeautifulSoup(website.content, 'html.parser')
        teamsInLeague = soupPage.find(
            class_="table table-hover table-bordered").find('tbody')
        for team in teamsInLeague('tr'):
            teamData = team.find_all('td')
            tourneys[tourneyID]['Teams'].append({
                "Name": teamData[1].getText(),
                "Wins": teamData[2].getText(),
                "Place": teamData[0].getText(),
                "Team_Link": "https://dota.playon.gg" + teamData[1].find('a')['href'],
                'Division_Link': tourneyURL,
                'Division_Number': tourneyURL.split('/')[-1]
            })
    print("AD2L Teams Loaded")
    return tourneys
