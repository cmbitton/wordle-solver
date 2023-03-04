from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time 
from words import words

STARTING_WORD = "drive"
LETTER_VALUES = {'a': 8.46, 'b': 2.48, 'c': 4.16, 'd': 3.45, 'e': 9.83, 'f': 1.92, 'g': 2.79, 'h': 3.52, 'i': 6.03, 'j': 0.25, 'k': 1.89, 'l': 6.02, 'm': 2.78, 'n': 5.12, 'o': 6.27, 'p': 3.22, 'q': 0.27, 'r': 7.79, 's': 5.76, 't': 6.23, 'u': 4.26, 'v': 1.38, 'w': 1.8, 'x': 0.35, 'y': 3.88, 'z': 0.33}

class Word_Reduction:
    def __init__(self, word_list, letters, letter_states, guessed_word):
        self.word_list = word_list
        self.letters = letters
        self.letter_states = letter_states
        self.guessed_word = guessed_word
    
    def get_repeat_letter_states(self, index):
        if self.guessed_word.count(self.letters[index].lower()) > 1:
            indexes = [j for j in range(5) if self.guessed_word.startswith(self.letters[index].lower(), j)]
            repeat_letter_states = []
            for num in indexes:
                repeat_letter_states.append(self.letter_states[num])
            return repeat_letter_states
        
    def filter_words_containing_current_letter(self, index):
        self.word_list = [word for word in self.word_list if self.letters[index].lower() not in word]
    
    def filter_words_containing_letter_at_index(self, index):
        self.word_list = [word for word in self.word_list if self.letters[index].lower() != word[index]]
    
    def filter_word_list(self):
        for i in range(5):
            if self.letter_states[i] == "absent":
                repeat_letter_states = self.get_repeat_letter_states(i)
                if repeat_letter_states:
                    if "present" not in repeat_letter_states and "correct" not in repeat_letter_states:
                        self.filter_words_containing_current_letter(i)
                    else:
                        self.filter_words_containing_letter_at_index(i)
                else:
                    self.filter_words_containing_current_letter(i)
            elif self.letter_states[i] == "correct":
                self.word_list = [word for word in self.word_list if word[i].lower() == self.letters[i].lower()]
                repeat_letter_states = self.get_repeat_letter_states(i)
                if repeat_letter_states:
                    if "absent" in repeat_letter_states:
                        self.word_list = [word for word in self.word_list if self.letters[i].lower() not in word[:i] and self.letters[i].lower() not in word[i+1:]]
            
            elif self.letter_states[i] == "present":
                self.word_list = [word for word in self.word_list if self.letters[i].lower() in word]
                self.filter_words_containing_letter_at_index(i)
        return self.word_list


class Main:
    def __init__(self):
        self.wordle_guess = STARTING_WORD
        self.word_list = words
        self.driver = webdriver.Chrome('/chromedriver')

    def open_wordle_website(self):
        self.driver.implicitly_wait(0.5)
        self.driver.maximize_window()
        self.driver.get('https://www.nytimes.com/games/wordle/index.html')
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def close_instructions(self):
        close_instruction = self.driver.find_element(By.CSS_SELECTOR, "svg.game-icon")
        close_instruction.click()
        time.sleep(1)
        self.body = self.driver.find_element(By.CSS_SELECTOR, "body")
        self.body.click()

    def enter_word(self):
        self.body.send_keys(self.wordle_guess, Keys.ENTER)
        time.sleep(3)
    
    def get_letter_states(self, tile_list):
        letter_states = {}
        for i in range(5):
            letter_states[i] = tile_list[i].get_attribute('data-state')
        return letter_states

    def get_letters(self, tile_list):
        letters = {}
        for i in range(5):
            letters[i] = tile_list[i].text
        return letters
    
    def return_letters_and_letter_states(self, index):
        tiles = self.driver.find_elements(By.CSS_SELECTOR, f"div[aria-label='Row {index + 1}'] div div")
        letters = self.get_letters(tiles)
        letter_states = self.get_letter_states(tiles)
        return letters, letter_states

    def log_round_results(self, letters, letter_states):
        print(letters, letter_states)
        print(len(self.word_list))
        print(self.word_list)

    def calculateHighestValueWord(self):
        highest_value = 0
        best_word = ""
        for word in self.word_list:
            current_value = 0
            word_set = set(word)
            for letter in word_set:
                current_value += LETTER_VALUES[letter]
            if current_value > highest_value:
                best_word = word
                highest_value = current_value
        return best_word
    
    def check_for_win(self, letter_states):
        correct_letters = 0
        for state in letter_states:
            if letter_states[state] == "correct":
                correct_letters += 1
        if correct_letters == 5:
            return True
    
    def run_main(self):
        self.open_wordle_website()
        self.close_instructions()
        for i in range(6):
            self.enter_word()
            letters, letter_states = self.return_letters_and_letter_states(i)
            self.log_round_results(letters, letter_states)
            self.word_list = Word_Reduction(self.word_list, letters, letter_states, self.wordle_guess).filter_word_list()
            if self.check_for_win(letter_states):
                time.sleep(30)
                quit()
            self.wordle_guess = self.calculateHighestValueWord()
        
main = Main()
main.run_main()
