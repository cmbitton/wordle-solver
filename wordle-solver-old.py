from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time 

correct_letters = []
valid_letters = []
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

#sorts letters into wordle helper
def sort_letters():
    global correct_letters
    global valid_letters
    for i in range(5):
        if letter_states[i] == 'correct':
            correct_letter = driver.find_element(By.CSS_SELECTOR, f"div#good-letters input[data-index='{i}']")
            correct_letter.send_keys(f"${letters[i]}")
            correct_letters += letters[i]
        elif letter_states[i] == 'present':
            present_letters = driver.find_element(By.CSS_SELECTOR, f"div#valid-letters input[data-index='{i+5}']")
            present_letters.send_keys(f"${letters[i]}")
            valid_letters += letters[i]
    for i in range(5):
        if letter_states[i] == 'absent':
            if letters[i] in correct_letters or letters[i] in valid_letters:
                continue
            bad_letters = driver.find_element(By.CSS_SELECTOR, 'div#bad-letters input:not(.bad)')
            bad_letters.send_keys(f"${letters[i]}")

#gets the next word from wordle helper
def get_next_word():
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, 'a[data-action="search"]').click()
    time.sleep(2)
    next_letters = driver.find_elements(By.CSS_SELECTOR, '#ws-results div.row div.ws-result:first-child span')
    next_word = ''
    for letter in next_letters:
        next_word += letter.text
    return next_word
       
#checks for win
def check_for_win(letter_states):
    correct_letters = 0
    for state in letter_states:
        if letter_states[state] == "correct":
            correct_letters += 1
    if correct_letters == 5:
        return True

def remove_found_letters():
    valid_letters = driver.find_elements(By.CSS_SELECTOR, f"div#valid-letters input")
    correct_letters = driver.find_elements(By.CSS_SELECTOR, f"div#good-letters input")
    for i in range(5):
        valid_letters[i].clear()
        correct_letters[i].clear()
        driver.execute_script(f"""
        const validLetters= [...document.querySelectorAll('div#valid-letters input.valid')];
        for(const letter of validLetters) letter.classList.remove('valid')
        """)

FIRST_WORD = 'momma'
driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(0.5)
driver.maximize_window()
driver.get('https://www.nytimes.com/games/wordle/index.html')
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
#closes instructions for game
close_instruction = driver.find_element(By.CSS_SELECTOR, "svg.game-icon")
close_instruction.click()
time.sleep(1)
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
if check_for_win(letter_states):
    time.sleep(30)
    quit()

#opens new window and switches to wordle helper
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])
driver.get('https://www.thewordfinder.com/wordle-solver/')
time.sleep(2)

#sorts letters and gets next word
driver.find_element(By.CSS_SELECTOR, "input#strict").click()
remove_found_letters()
sort_letters()

next_word = get_next_word()

#switch window and guess 2nd word
driver.switch_to.window(driver.window_handles[0])
time.sleep(1)
body.send_keys(next_word, Keys.ENTER)
time.sleep(3)

#gets letters, states, and tiles and checks for win
tiles = driver.find_elements(By.CSS_SELECTOR, "div[aria-label='Row 2'] div div")
letters = get_letters(tiles)
letter_states = get_letter_states(tiles)
if check_for_win(letter_states):
    time.sleep(30)
    quit()

#switch to wordle helper, sort letters, and get next word
driver.switch_to.window(driver.window_handles[1])
time.sleep(1)
remove_found_letters()
sort_letters()
next_word = get_next_word()

#switch to wordle, input 3rd word
driver.switch_to.window(driver.window_handles[0])
time.sleep(1)
body.send_keys(next_word, Keys.ENTER)
time.sleep(3)

#gets letters, states, and tiles and checks for win
tiles = driver.find_elements(By.CSS_SELECTOR, "div[aria-label='Row 3'] div div")
letters = get_letters(tiles)
letter_states = get_letter_states(tiles)
if check_for_win(letter_states):
    time.sleep(30)
    quit()

#switch to wordle helper, sort letters, and get next word
driver.switch_to.window(driver.window_handles[1])
time.sleep(1)
remove_found_letters()
sort_letters()
next_word = get_next_word()

#switch to wordle, input 4th word
driver.switch_to.window(driver.window_handles[0])
time.sleep(1)
body.send_keys(next_word, Keys.ENTER)
time.sleep(3)

#gets letters, states, and tiles and checks for win
tiles = driver.find_elements(By.CSS_SELECTOR, "div[aria-label='Row 4'] div div")
letters = get_letters(tiles)
letter_states = get_letter_states(tiles)
if check_for_win(letter_states):
    time.sleep(30)
    quit()

#switch to wordle helper, sort letters, and get next word
driver.switch_to.window(driver.window_handles[1])
time.sleep(1)
remove_found_letters()
sort_letters()
next_word = get_next_word()

#switch to wordle, input 5th word
driver.switch_to.window(driver.window_handles[0])
time.sleep(1)
body.send_keys(next_word, Keys.ENTER)
time.sleep(3)

#gets letters, states, and tiles and checks for win
tiles = driver.find_elements(By.CSS_SELECTOR, "div[aria-label='Row 5'] div div")
letters = get_letters(tiles)
letter_states = get_letter_states(tiles)
if check_for_win(letter_states):
    time.sleep(30)
    quit()

#switch to wordle helper, sort letters, and get next word
driver.switch_to.window(driver.window_handles[1])
time.sleep(1)
remove_found_letters()
sort_letters()
next_word = get_next_word()

#switch to wordle, input final word
driver.switch_to.window(driver.window_handles[0])
time.sleep(1)
body.send_keys(next_word, Keys.ENTER)
time.sleep(30)