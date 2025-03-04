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
