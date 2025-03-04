# ASL Flash Card Application
A Python-based flashcard application designed to help users learn American Sign Language (ASL). This project uses a polished, image-based interface built with Tkinter and leverages Selenium to look up ASL signs on Google. The app tracks your progress over time, adapting the frequency of flashcards based on your performance.

---

## Features

- **Image-Based GUI:**  
  Flash cards with attractive background images for the front and back of the card.

- **Adaptive Learning:**  
  Words that you answer incorrectly appear more frequently to reinforce learning.

- **Selenium Integration:**  
  When you mark a word as "wrong," a new browser tab opens via Selenium showing the ASL sign on Google. The tab remains open until you interact with the next card, at which point it automatically closes.

- **Progress Tracking:**  
  Your right and wrong counts are saved to a JSON file (`progress.json`), so your learning progress persists between sessions.

- **User-Friendly Interface:**  
  Simple button controls allow you to mark your responses and reveal ASL signs, making it easy to use.

---

## Requirements

- **Python 3.x**
- **Chrome Browser**
- **Chromedriver:**  
  [Download Chromedriver](https://chromedriver.chromium.org/downloads) and ensure it is available in your system's PATH.

- **Python Packages:**
  - [Selenium](https://pypi.org/project/selenium/)
  - [pandas](https://pypi.org/project/pandas/)
  - Tkinter (usually included with Python)

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/gajanan229/ASL-Flash-Cards.git
   cd ASL-Flash-Cards
   ```

2. **Install Required Packages:**

   ```bash
   pip install selenium pandas
   ```

3. **Set Up Chromedriver:**

   Download Chromedriver from [here](https://chromedriver.chromium.org/downloads) and ensure it is in your PATH or in the project directory.

4. **Prepare Image Assets:**

   Create an `images` folder and add the following image files:
   - `card_front.png` (Flashcard front background)
   - `card_back.png` (Flashcard back background)
   - `right.png` (Image for "Right" button)
   - `wrong.png` (Image for "Wrong" button)

5. **CSV Vocabulary File:**

   Place your CSV file (e.g., `ASL1.4_vocab - Sheet1.csv`) in the project directory. Ensure the CSV file has a header row and the ASL words in the first column.

---

## Usage

Run the application with:

```bash
python app.py
```

### How It Works

- **Flash Card Display:**  
  A flash card with the current ASL word is displayed on the GUI.

- **Marking Responses:**
  - **I Got It Right:**  
    Increments the "right" count for the word.
  - **I Got It Wrong:**  
    Increments the "wrong" count, opens a new Selenium tab with a Google search for the ASL sign and then moves to the next card.
  - **Show ASL Sign:**  
    Opens the ASL sign lookup in a new Selenium tab without recording a wrong answer.

- **Tab Management:**  
  The lookup tab opened via Selenium remains open until you interact with the new card (via any button), at which point the previous lookup tab is closed automatically.

- **Progress Saving:**  
  Your learning progress is automatically saved to `progress.json` every time you mark a card and when you close the application.

---

## Project Structure

```
ASL-Flash-Cards/
├── app.py                        # Main application code
├── ASL1.4_vocab - Sheet1.csv     # CSV file with ASL vocabulary
├── progress.json                 # JSON file for saving progress (auto-generated)
├── images/
│   ├── card_front.png            # Flash card front image
│   ├── card_back.png             # Flash card back image
│   ├── right.png                 # "Right" button image
│   └── wrong.png                 # "Wrong" button image
└── README.md                     # This file
```

---
