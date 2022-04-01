from threading import Thread
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import asyncio
import os
from multiprocessing import Process
from time import sleep


def getImageProfile(userID):
    options = webdriver.ChromeOptions()
    options.headless = True
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f'https://stratz.com/players/{userID}')

    WebDriverWait(driver, 10).until(lambda driver: driver.execute_script(
        'return document.readyState') == 'complete')
    sleep(1)
    driver.set_window_size(1920, 1080)
    while(True):
        try:
            driver.find_element(
                by=By.XPATH, value='//html/body/div[2]/main/div[3]/div[3]/div/div[1]/div/div/button[2]').click()
            break
        except:
            sleep(1)

    sleep(5)
    # driver.find_element(by=By.TAG_NAME, value='body').screenshot(
    #    f'{userID}.png')
    driver.find_element(
        by=By.XPATH, value='//*[@id="root"]/main/div[3]/div[3]/div').screenshot(f'{os.getcwd()}/images/temp/{userID}.png')
    driver.close()
    print(f"Done with {userID}")


def profiles():
    users = [90143300, 119088315, 106790655, 101387028]
    for user in users:
        p = Process(target=getImageProfile, args=(user,)).start()


if __name__ == '__main__':
    profiles()
