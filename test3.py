import requests
from bs4 import BeautifulSoup


def getDotabuffStats(player_ID):
    # Got my own user agent to stop web-scraping prevention
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.36'}
    website = requests.get(
        f'https://www.dotabuff.com/esports/players/{player_ID}', headers=headers)
    # Soup Webiste
    soupWebsite = BeautifulSoup(website.content, "html.parser")
    rolesBar = soupWebsite.find(class_='roles bar')
    roleSplits = {
        'Core': {
            'Total': 0,
            'Off Lane': 0,
            'Roaming': 0,
            'Mid Lane': 0,
            'Jungle': 0,
            'Safe Lane': 0
        },
        'Support': {
            'Total': 0,
            'Off Lane': 0,
            'Roaming': 0,
            'Mid Lane': 0,
            'Jungle': 0,
            'Safe Lane': 0
        }
    }
    mostCommonRoleTotal = rolesBar.find(
        class_='sector role index-0').find(class_='label').getText()
    print(mostCommonRoleTotal)
    supportAndCoreBreakdown = rolesBar.find_all(class_='tooltip')
    for role in supportAndCoreBreakdown:
        whereToAdd = role.find(class_='header').getText().split(" ")[0]
        for currentClass in role:
            if currentClass == "header":
                None
