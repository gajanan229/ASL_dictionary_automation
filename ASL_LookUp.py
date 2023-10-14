import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set up Chrome with detach option so it doesnt close on completion
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

# Open and read a CSV file
with open("ASL1.4_vocab - Sheet1.csv", 'r') as file:
    csvread = csv.reader(file)
    for idx, word in enumerate(csvread):

        # Join elements in the row to create a search word
        search_word = ''.join(map(str, word))
        search_query = f"{search_word} in ASL"

        # Checks if it's not the first row, if not it will open new tab and switch to it
        if idx != 0 :
            driver.execute_script("window.open('about:blank', '_blank');")
            driver.switch_to.window(driver.window_handles[idx])

        # Load Google search results page for the current search word
        driver.get(f"https://www.google.com/search?q={search_word}+in+ASL")


