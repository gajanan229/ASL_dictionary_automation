from tkinter import *
import pandas
import random
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BACKGROUND_COLOR = "#B1DDC6"

class FlashCardApp:
    def __init__(self, master, csv_file, progress_file="progress.json"):
        self.master = master
        self.csv_file = csv_file
        self.progress_file = progress_file
        self.words = self.load_words()  # Load words from CSV into a dictionary.
        self.load_progress()            # Merge any saved progress.
        self.current_word = None
        self.flip_timer = None
        self.lookup_tab = None

        # Initialize Selenium WebDriver.
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.main_handle = self.driver.window_handles[0]

        # Set up the main window.
        self.master.title("ASL Flash Cards")
        self.master.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

        # Load images.
        self.card_front_img = PhotoImage(file="images/card_front.png")
        self.card_back_img = PhotoImage(file="images/card_back.png")
        self.right_img = PhotoImage(file="images/right.png")
        self.wrong_img = PhotoImage(file="images/wrong.png")

        # Create the canvas to display the flash card.
        self.canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.card_background = self.canvas.create_image(400, 263, image=self.card_front_img)
        self.card_title = self.canvas.create_text(400, 150, text="ASL", font=("Ariel", 40, "italic"))
        self.card_word = self.canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
        self.canvas.grid(row=0, column=0, columnspan=3)

        # Create buttons.
        self.wrong_button = Button(image=self.wrong_img, highlightthickness=0, command=self.got_it_wrong)
        self.wrong_button.grid(row=1, column=0)

        # A button to show the sign (which flips the card and opens a Google search).
        self.show_button = Button(text="Show ASL Sign", command=self.show_sign, width=20)
        self.show_button.grid(row=1, column=1)

        self.right_button = Button(image=self.right_img, highlightthickness=0, command=self.got_it_right)
        self.right_button.grid(row=1, column=2)

        # Label to display progress.
        self.progress_label = Label(text="", bg=BACKGROUND_COLOR, font=("Ariel", 12))
        self.progress_label.grid(row=2, column=0, columnspan=3)

        # Start with the first card.
        self.next_card()

        # Save progress automatically on window close.
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_words(self):
        """
        Load words from a CSV file.
        The CSV should have a header row and the word in the first column.
        Each word is stored with counters for right and wrong attempts.
        """
        words = {}
        # Using pandas to read the CSV file.
        data = pandas.read_csv(self.csv_file)
        for index, row in data.iterrows():
            word = str(row[0]).strip()
            words[word] = {"right": 0, "wrong": 0}
        return words

    def load_progress(self):
        """
        Load progress from a JSON file (if it exists) and update the words dictionary.
        """
        if os.path.exists(self.progress_file):
            with open(self.progress_file, "r", encoding="utf-8") as f:
                progress_data = json.load(f)
            # Update progress for words that exist in the CSV.
            for word, stats in progress_data.items():
                if word in self.words:
                    self.words[word] = stats

    def save_progress(self):
        """
        Save current progress (right/wrong counts) to a JSON file.
        """
        with open(self.progress_file, "w", encoding="utf-8") as f:
            json.dump(self.words, f, indent=2)
        print("Progress saved.")

    def calculate_weight(self, word):
        """
        Calculate the selection weight for a word.
        More wrong answers (relative to right ones) increase the chance of being chosen.
        """
        stats = self.words[word]
        return (1 + stats["wrong"]) / (1 + stats["right"])

    def close_lookup_tab_if_exists(self):
        """
        Close any previously opened lookup tab if it exists.
        This should be called at the start of any new action for the new card.
        """
        if self.lookup_tab is not None:
            try:
                self.driver.switch_to.window(self.lookup_tab)
                self.driver.close()
            except Exception as e:
                print(f"Error closing lookup tab: {e}")
            self.driver.switch_to.window(self.main_handle)
            self.lookup_tab = None

    def next_card(self):
        """
        Select the next word based on the weights and update the flash card display.
        """
        if self.flip_timer:
            self.master.after_cancel(self.flip_timer)
        words_list = list(self.words.keys())
        weights = [self.calculate_weight(word) for word in words_list]
        self.current_word = random.choices(words_list, weights=weights, k=1)[0]
        # Set the flash card to the front image with the current word.
        self.canvas.itemconfig(self.card_background, image=self.card_front_img)
        self.canvas.itemconfig(self.card_title, text="ASL", fill="black")
        self.canvas.itemconfig(self.card_word, text=self.current_word, fill="black")
        stats = self.words[self.current_word]
        self.progress_label.config(text=f"Right: {stats['right']}   Wrong: {stats['wrong']}")
        # (Optional) You could set a timer here to auto-flip after a delay.
        # self.flip_timer = self.master.after(3000, self.flip_card)

    def flip_card(self):
        """
        Flip the flash card to show the back image and change text style.
        """
        self.canvas.itemconfig(self.card_background, image=self.card_back_img)
        self.canvas.itemconfig(self.card_title, text="ASL Sign", fill="white")
        # Clear the word text if desired or you could show additional info.
        self.canvas.itemconfig(self.card_word, text="", fill="white")

    def show_sign(self):
        """
        Flip the card and open a browser to show the ASL sign on Google.
        """
        # Close any lookup tab from a previous card.
        self.close_lookup_tab_if_exists()
        self.flip_card()
        search_query = f"{self.current_word} in ASL"
        url = f"https://www.google.com/search?q={search_query}"
        # Open a new tab via Selenium and store its handle.
        self.driver.execute_script("window.open('about:blank', '_blank');")
        self.lookup_tab = self.driver.window_handles[-1]
        self.driver.switch_to.window(self.lookup_tab)
        self.driver.get(url)

    def got_it_right(self):
        """
        Record a correct attempt, save progress, and show the next card.
        """
        self.close_lookup_tab_if_exists()
        self.words[self.current_word]["right"] += 1
        self.save_progress()
        self.next_card()

    def got_it_wrong(self):
        """
        Record an incorrect attempt, save progress, show the sign, and then the next card.
        """
        self.close_lookup_tab_if_exists()
        self.words[self.current_word]["wrong"] += 1
        self.save_progress()
        # Open lookup tab for the current (wrong) card.
        search_query = f"{self.current_word} in ASL"
        url = f"https://www.google.com/search?q={search_query}"
        self.driver.execute_script("window.open('about:blank', '_blank');")
        self.lookup_tab = self.driver.window_handles[-1]
        self.driver.switch_to.window(self.lookup_tab)
        self.driver.get(url)
        # Switch to the next card; the lookup tab remains open until a new action is taken.
        self.next_card()

    def on_close(self):
        """
        Save progress when the window is closed.
        """
        self.save_progress()
        # Attempt to close any open lookup tab.
        self.close_lookup_tab_if_exists()
        self.driver.quit()
        self.master.destroy()

if __name__ == "__main__":
    root = Tk()
    # Replace "ASL1.4_vocab - Sheet1.csv" with your CSV file path.
    app = FlashCardApp(root, "ASL1.4_vocab - Sheet1.csv")
    root.mainloop()