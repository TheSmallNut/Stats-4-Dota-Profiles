import requests
from bs4 import BeautifulSoup


def getCaptain(soup):
    return soup.find_all(class_="col-sm-10")[1].find('a').get('href').split("/")[-1]


URL = f'https://dota.playon.gg/teams/14217'
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")


results = soup.find(class_="rosterholder").find('ul').find_all('li')

DotaIDS = []
for player in results:
    DotaIDS.append(int(player.find_all('a')[0].get('href').split("/")[-1]))

toReturn = {
    'Captain': getCaptain(soup),
    'Players': DotaIDS
}
