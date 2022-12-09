from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time 

FIRST_WORD = 'fixer'
driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(0.5)
driver.get('https://www.nytimes.com/games/wordle/index.html')
#closes instructions for game
close_instruction = driver.find_element(By.CSS_SELECTOR, "svg.game-icon")
close_instruction.click()