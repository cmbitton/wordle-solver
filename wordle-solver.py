from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time 
#functions

#gets the state of the letters (correct, present, absent)
def get_letter_states(tile_list):
    letter_states = {}
    for i in range(5):
        letter_states[i] = tile_list[i].get_attribute('data-state')
    return letter_states
#gets the value of the letters in the word (a,b,c,d...)
def get_letters(tile_list):
    letters = {}
    for i in range(5):
        letters[i] = tile_list[i].text
    return letters

def sort_letters():
    for i in range(5):
        if letter_states[i] == 'correct':
            letter = driver.find_element(By.CSS_SELECTOR, f"div#good-letters input[data-index='{i}']")
            letter.send_keys(f"${letters[i]}")
        elif letter_states[i] == 'absent':
            bad_letters = driver.find_element(By.CSS_SELECTOR, 'div#bad-letters input:not(.bad)')
            bad_letters.send_keys(f"${letters[i]}")
        elif letter_states[i] == 'present':
            present_letters = driver.find_element(By.CSS_SELECTOR, f"div#valid-letters input[data-index='{i+5}']")
            present_letters.send_keys(f"${letters[i]}")

def get_next_word():
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(2)
    next_word = driver.find_element(By.CSS_SELECTOR, '#result-cards div.flex-wrap span span').text
    return next_word

FIRST_WORD = 'fiber'
driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(0.5)
driver.get('https://www.nytimes.com/games/wordle/index.html')
#closes instructions for game
close_instruction = driver.find_element(By.CSS_SELECTOR, "svg.game-icon")
close_instruction.click()
time.sleep(2)
#clicks body to allow word to be entered
body = driver.find_element(By.CSS_SELECTOR, "body")
body.click()
#types in first word
body.send_keys(FIRST_WORD, Keys.ENTER)
time.sleep(3)

#grabs all letter boxes (div), letter values (a,b,c,d...), and letter states (absent, present, correct)
tiles = driver.find_elements(By.CSS_SELECTOR, "div[aria-label='Row 1'] div div")
letters = get_letters(tiles)
letter_states = get_letter_states(tiles)

#opens new window and switches to wordle helper
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])
driver.get('https://www.thewordfinder.com/wordle-solver/')
time.sleep(2)
sort_letters()
time.sleep(1)