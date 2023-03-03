# Automated Wordle Solver

Automated Wordle Solver is a web automation bot written in Python that utilizes Selenium

-----------------------------------------

### How To Use

Download the project folder and install all requirements. Simply run the wordle-solver-automatic.py file to
start the bot with the default starting word. If you want to change the starting word, simple change the "word"
variable within the file.

<b>Note: </b>The wordle-solver.py program uses a 3rd part website to filter the word list, and is no longer supported.
The algorithm based approach is more reliable and does not require any third party sites besides NYT.

-----------------------------------------

### How It Works

First, a browser instance is created using Selenium, which navigates to the New York Times' Wordle page. The bot then exits the Wordle instructions and enters the first word. The bot records and processes the results from the first word using a reduction algorithm, which continuously filters down a list of possible words. Each word in the list of possible words is assigned a score based on its letter frequency within the list of all possible words. The word with the highest score is chosen from the list of possible words to be used for the next iteration, and the process is repeated until a solution is found.

### List Coming Soon
