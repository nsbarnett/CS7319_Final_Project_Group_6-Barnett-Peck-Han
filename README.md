# EmoBot - A Pygame-based Emotional Support Chatbot

## Description

**EmoBot** is a graphical chatbot built using Python and Pygame. It combines a conversational AI model with an interactive, calming user interface. EmoBot supports user profiles, mood tracking, and plays background music to create a relaxing experience.

---

## Features

- 💬 Chat interface with GPT-powered responses
- 😊 Mood check-ins before and after each chat
- 👤 Profile system with persistent data (`profiles.json`)
- 🎵 Lofi background music for relaxation
- 🖱️ Clickable buttons for easy navigation
- 🔇 Toggle sound or pause session
- 📈 Tracks emotional state improvements

---

## Requirements

- Python 3.x
- [pygame](https://www.pygame.org/)

### Required Assets (in `/assets/` folder):
- `Play Rect.png`
- `Quit Rect.png`
- `profile_button.png`
- `round-button.png`
- `end_session.png`
- `font.ttf`
- `lofi-background-music-1.mp3`
- `bot_icon.jpg`

### Modules:
- `chat_bot.py` – Main app file (Pygame UI)
- `chatbot.py` – Manages OpenAI chatbot logic
- `button.py` – Custom clickable button logic
- `profile.py` – Handles profile data structure and conversion

---

## Getting Started

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install pygame openai

