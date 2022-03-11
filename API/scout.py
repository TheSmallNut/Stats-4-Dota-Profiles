from matplotlib.image import thumbnail
import requests
from bs4 import BeautifulSoup
import json


def getDotaIDS(teamLink):
    URL = f'{teamLink}'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find_all(class_="DotabuffIcon")

    DotaIDS = []
    for player in results:
        DotaIDS.append(int(player.get('href').split("/")[-1]))
    return DotaIDS


def IDToDotabuff(id, esports=True):
    if esports:
        return f'https://www.dotabuff.com/esports/players/{id}'
    else:
        return f'https://www.dotabuff.com/players/{id}'


def recentHeroesPlayed(account_id):
    url = f'https://api.opendota.com/api/heroes'
    heroes = requests.get(url).json()
    url = f'https://api.opendota.com/api/players/{account_id}/recentMatches'
    recentMatches = requests.get(url).json()


def playerProfile(account_id):
    url = f'https://api.opendota.com/api/players/{account_id}'
    playerData = requests.get(url).json()
    playerName = playerData['profile']['personaname']
    thumbnail = playerData['profile']['avatarfull']
    icon_url = playerData['profile']['avatar']
    rank = playerData['rank_tier']
    steam = playerData['profile']['profileurl']
    return {
        'playerName': playerName,
        'thumbnail': thumbnail,
        'rank': rank,
        'steam': steam,
        'icon_url': icon_url
    }
