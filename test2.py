from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import asyncio
import os


# def S(X): return driver.execute_script(
#    'return document.body.parentNode.scroll' + X)


#driver.set_window_size(S('Width'), S('Height'))


# stratzButton[0].click()
#driver.find_element(by=By.TAG_NAME, value='body').screenshot('screenshot.png')

# driver.find_element(by=By.CLASS_NAME, value='sc-gsTCUz sc-jrAGrp dZuJve bJtIwT').screenshot('screenshot.png')


async def getImageProfile(userID):
    options = webdriver.ChromeOptions()
    options.headless = True
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f'https://stratz.com/players/{userID}')

    WebDriverWait(driver, 10).until(lambda driver: driver.execute_script(
        'return document.readyState') == 'complete')
    await asyncio.sleep(1)
    driver.set_window_size(1920, 1080)
    while(True):
        try:
            driver.find_element(
                by=By.XPATH, value='//html/body/div[2]/main/div[3]/div[3]/div/div[1]/div/div/button[2]').click()
            break
        except:
            await asyncio.sleep(1)

    await asyncio.sleep(5)
    # driver.find_element(by=By.TAG_NAME, value='body').screenshot(
    #    f'{userID}.png')
    driver.find_element(
        by=By.XPATH, value='//*[@id="root"]/main/div[3]/div[3]/div').screenshot(f'{os.getcwd()}/images/temp/{userID}.png')
    driver.close()
    print(f"Done with {userID}")


async def callFunctions():
    users = [90143300, 119088315, 106790655, 101387028]
    loops = []
    for user in users:
        loops.append(loop.create_task(getImageProfile(user)))
    await asyncio.wait(loops)


loop = asyncio.get_event_loop()
loop.run_until_complete(callFunctions())
loop.close()
print("DONE")
