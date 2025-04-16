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
2. **Install dependencies in terminal**:
   ```bash
   pip install pygame openai ngrok uvicorn fastapi
3. **For the OO architecture:**:
   - Ensure you are in the correct directory (./EmoBot/Selected)
   - Run
   ```bash
   python .\object_oriented_chatbot.py
4. **Navigate to the project directory via terminal**
5. **Run in terminal**
   - uvicorn prompt:app --reload
6. **In a new terminal tab, run the following**
   - ngrok http --url=winning-related-primate.ngrok-free.app 8000
   - Now the server is exposed to the internet at port 8000
7. **For client_server_chatbot.py, obtain an OpenAI API key and save it in a .env file with the following format**
   - OPEN_API_KEY=your-api-key-here
8. **Put the .env file in the project directory**

## Architecture Comparison: Client-Server vs. OOP
## Client-Server Architecture
In this architecture, the system is divided into two distinct layers:

-**Client Side**: Our front-end application runs a UI Handler that collects user input and sends it to the backend. It communicates with the server using an HTTP POST request tunneled through 'Ngrok'.

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

- `ChatBot`: central orchestrator for generating responses, uses gpt-4 model, a generated API key, and hard-coded written instructions.
- `Profile`: stores the user’s mood and chat history
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

## Graduate Requirement: In-Depth Analysis

For our AI mental health app, we evaluated using two architectural styles: client-server and object-oriented programming (OOP). The client-server model uses a FastAPI backend to host our fine-tuned OpenAI model, with Ngrok providing temporary public access for prototyping. This architecture separates the UI from the AI logic, supporting modularity, scalability, and remote collaboration. We implemented it in this way, as in actual development, we will want to use a more powerful model that does not have as much latency as our current model. We will also use faster connectors than FastAPI and Ngrok, as there was a problem with latency in our testing. Ngrok proved to be a slow connector for deployment, but adequate for prototyping. For actual deployment, our team would utilize Amazon Web Services to host the server for faster response times. Amazon Web Services also allows for very fast model throughput, utilizing the computational power of the cloud to process user input and give an AI agent's response. Furthermore, the client-server architecture allows for freedom of model selection. We used OpenAI's 4o-mini model as it was convenient, but models can also be hosted locally on a powerful server as well. There is freedom of local or remote models with client-server architecture.

The OOP architecture experienced much lower latency, but is less scalable than the client-server architecture. Since the OOP architecture depends on the computational power of the user's machine, the usage of any large language models is not advised. We found that the client-server architecture allows for better separation of concerns, easier maintenance, and external access, though it does require stronger models and depends on the reliability of API's and the machine that the server is hosted on. OOP allows for easier modularity and performs better for a single, local use, but lacks the scalability of a client-server architecture. Ultimately, we recommend a hybrid approach, leveraging the client-server architecture for AI services (ideally hosted in the cloud rather than on our laptops) and OOP for the client-side encapsulated logic. 
