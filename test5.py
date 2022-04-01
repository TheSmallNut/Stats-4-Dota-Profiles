import requests


def add(num1, num2):
    return num1 + num2


def getWebsite(url):
    return requests.get(url).text
