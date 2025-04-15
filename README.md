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
- OpenAI API Key (https://platform.openai.com/api-keys)
  - **FOR GRADER: If you have issues with generating an API key, please contact me at nsbarnett@smu.edu.**

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

## Architecture Comparison: Client-Server vs. OOP
## Client-Server Architecture
In this architecture, the system is divided into two distinct layers:

-**Client Side**: Our front-end application runs a UI Handler that collects user input and sends it to the backend. It communications with the server using an HTTP POST request tunneled through 'Ngrok'.

-**Server Side**: The backend is implemented using FastAPI. It routes requests through 'prompt.py', which then delegates tasks to internal services such as our **ChatBot** and **aspiration gengeator**, both powered by GPT-4o-mini.

### Mapped Files and Classes
| Component            | Class / File                | Description                                                  |
|----------------------|-----------------------------|--------------------------------------------------------------|
| UI Handler           | `client_server_chatbot.py`  | Captures input and sends POST request                        |
| API Gateway          | `prompt.py`                 | Routes input to GPT-4o-mini via FastAPI                      |
| GPT-4o-mini (chat)   | `OpenAI API`                | Returns contextual chatbot replies                           |
| GPT-4o-mini (aspiration) | `OpenAI API`             | Returns affirmation based on user's emotional state          |

This approach ensures clean separation between UI and business logic, and supports distributed deployment.

---

## Object-Oriented Programming (OOP)

In parallel, we also structured the project using OOP principles. Each core functionality is implemented as a class:

- `ChatBot`: central orchestrator for generating responses
- `Profile`: stores user’s mood and history
- `SentimentAnalyzer` and `AffirmationGenerator`: embedded as logic inside the chatbot
- UI elements are managed using `Button` and `object_oriented_chatbot.py`

### OOP Class Mapping Summary

| Module / Object         | Mapped Class(es)               | Description                                               |
|-------------------------|---------------------------------|-----------------------------------------------------------|
| UI Handler              | `Button`, `object_oriented_chatbot.py` | Captures input and displays output                   |
| ChatBot                 | `ChatBot`                       | Manages dialogue and routes logic                         |
| Sentiment Analyzer      | `ChatBot.instructions`          | Parses tone from user input                               |
| Affirmation Generator   | `ChatBot.instructions`          | Delivers positive affirmations                            |
| Chat History            | `ChatBot.chat_history`          | Stores interaction memory                                 |
| Feedback System         | `ChatBot.instructions`          | Learns from user responses                                |
| User Profile            | `Profile.pre_chat_mood`, etc.   | Tracks mood before and after chats                        |

This structure promotes encapsulation, modularity, and reusability—making it easier to test and extend functionality.

---

## Final Architecture Decision: Hybrid

We chose to **combine** both architectures in our final implementation:

- **Client-Server** architecture for deployment structure and API handling
- **OOP** design for internal code structure and logic organization

This hybrid approach gives us the best of both: scalability, clarity, and maintainability.
