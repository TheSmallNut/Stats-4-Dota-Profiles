import requests
from bs4 import BeautifulSoup
import json
from lxml import etree
from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import asyncio
import os
from selenium.webdriver.support import expected_conditions as EC


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


def getAD2LTeams(tourneyIDS):
    tourneys = {}
    for tourneyID in tourneyIDS:
        tourneyID = str(tourneyID)
        tourneyURL = f'https://dota.playon.gg/seasons/{tourneyID}'
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


def checkIfRegularSeason(tourneyPage):
    navbarHeader = tourneyPage.find(
        class_='navbar navbar-subnav navbar-ad2l container')
    navTabs = navbarHeader.find(class_='nav nav-tabs')
    tabs = navTabs.find_all(class_='tab')
    firstTab = tabs[0].find('a').getText()
    if firstTab == 'Regular Season':
        return False
    return True


def getStratzPage(userID, sleepTime=10):
    options = webdriver.ChromeOptions()
    options.headless = True
    #service = Service(ChromeDriverManager().install())
    service = Service(ChromeDriverManager().install())
    # /Users/james/.wdm/drivers/chromedriver/mac64/99.0.4844.51/chromedriver
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f'https://stratz.com/players/{userID}')
    WebDriverWait(driver, 10).until(lambda driver: driver.execute_script(
        'return document.readyState') == 'complete')
    driver.set_window_size(1920, 1080)
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//html/body/div[2]/main/div[3]/div[3]/div/div[1]/div/div/button[2]')))
        print('FOUND BUTTON')
        driver.find_element(
            by=By.XPATH, value='//html/body/div[2]/main/div[3]/div[3]/div/div[1]/div/div/button[2]').click()
    except:
        print('Loading took too much time!')
    # driver.find_element(by=By.TAG_NAME, value='body').screenshot(
    #    f'{userID}.png')
    try:
        WebDriverWait(driver, sleepTime).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/main/div[3]/div[3]/div/div[2]/div/div[1]/div/svg/g[1]')))
        print('Element is ready')
    except:
        print('Loading took too much time!')
    sleep(1)
    driver.find_element(
        by=By.XPATH, value='//*[@id="root"]/main/div[3]/div[3]/div').screenshot(f'{os.getcwd()}/images/temp/{userID}.png')
    driver.close()
    print(f"Done with {userID}")
