from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.headless = True
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://www.dota2.com/springcleaning')


WebDriverWait(driver, 10).until(lambda driver: driver.execute_script(
    'return document.readyState') == 'complete')

sleep(10)


def S(X): return driver.execute_script(
    'return document.body.parentNode.scroll' + X)


driver.set_window_size(S('Width'), S('Height'))
#driver.set_window_size(1920, 1080)

#driver.find_element(
    #by=By.XPATH, value='//*[@id="root"]/main/div[3]/div[3]/div/div[1]/div/div/button[2]').click()
sleep(10)
# stratzButton[0].click()
driver.find_element(by=By.TAG_NAME, value='body').screenshot('screenshot.png')
#driver.find_element(
    #by=By.XPATH, value='//*[@id="root"]/main/div[3]/div[3]/div').screenshot('screenshot.png')
# driver.find_element(by=By.CLASS_NAME, value='sc-gsTCUz sc-jrAGrp dZuJve bJtIwT').screenshot('screenshot.png')

print("DONE")
