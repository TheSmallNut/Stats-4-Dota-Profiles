import requests
from bs4 import BeautifulSoup


# Grabbing a bunch of info from Opendota, example: https://api.opendota.com/api/players/90143300
def getOpenDotaStats(player_ID):
    url = f'https://api.opendota.com/api/players/{player_ID}'
    playerData = requests.get(url).json()
    playerName = playerData['profile']['personaname']
    icon_url = playerData['profile']['avatar']
    rank = playerData['rank_tier']
    steam = playerData['profile']['profileurl']
    leaderboard = playerData['leaderboard_rank']
    dotaplus = playerData['profile']['plus']
    country_code = playerData['profile']['loccountrycode']
    mmr_estimate = playerData['mmr_estimate']['estimate']
    return {
        'playerName': playerName,
        'rank': rank,
        'leaderboard': leaderboard,
        'steam_url': steam,
        'icon_url': icon_url,
        'dotaplus' : dotaplus,  # True / False
        'country_code' : country_code,
        'mmr_estimate' : mmr_estimate
    }


# Scraping what lane the player plays
def getDotabuffStats(player_ID):
    # Got my own user agent to prevent web-scraping prevention
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.36'}
    website = requests.get(f'https://www.dotabuff.com/esports/players/{player_ID}', headers = headers)
    # Soup Webiste
    soupWebsite = BeautifulSoup(website.content, "html.parser")
    rolesBar = soupWebsite.find(class_='roles bar')
    mostCommonRole = {
        'Core' : {
            'Total' : 0,
            'Off Lane' : 0,
            'Roaming' : 0,
            'Mid Lane' : 0,
            'Jungle' : 0,
            'Safe Lane' : 0
        },
        'Support' : {
            'Total' : 0,
            'Off Lane' : 0,
            'Roaming' : 0,
            'Mid Lane' : 0,
            'Jungle' : 0,
            'Safe Lane' : 0
        }
    }

    supportAndCoreBreakdown = rolesBar.find_all(class_='tooltip')
    for role in supportAndCoreBreakdown:
        whereToAdd = role.find(class_='header').getText().split(" ")[0]
        for currentClass in role:
            if currentClass == "header":
                print(currentClass)

    #mostCommonSplit = rolesBar.find(class_='sector role index-0').find(class_='label').getText().strip().split(" ")
    #mostCommonRole['Name'] = mostCommonSplit[1]
    #mostCommonRole['Percentage'] = mostCommonSplit[]


getDotabuffStats(119088315)

