Project Title: EmoBot - A Pygame-based Emotional Support Chatbot using OpenAI

Description:
    EmoBot is a graphical chatbot application built with Python and Pygame.
    It combines a conversational AI (via the ChatBot class) with a user-friendly
    interface, background music, profile management, and mood tracking. The goal
    is to create a calming and interactive emotional support environment.

Features:
    - Chat interface with AI-powered responses.
    - Mood check-ins before and after each chat session.
    - Profile system with persistence (via profiles.json).
    - Calming lofi background music during chats.
    - Visual buttons for interaction and navigation.
    - Option to toggle sound and pause the chat.
    - Mood improvement feedback after the chat.

Requirements:
    - Python 3.x
    - pygame
    - Assets (images and audio) in the /assets folder:
        -Play Rect.png, Quit Rect.png, profile_button.png,
        round-button.png, end_session.png
        - Font: assets/font.ttf
        - Background music: lofi-background-music-1.mp3
    I   - con: bot_icon.jpg

- External modules:
    - button.py: For handling clickable UI buttons
    - chatbot.py: For interacting with the chatbot API
    - profile.py: For handling profile creation and conversion to dictionary format

How to Run:
    1. Ensure all dependencies and assets are available.
    2. Run the script:
        python chat_bot.py
    3. Navigate the menus using your mouse:
        - Create/select a profile
        - Rate your mood
        - Begin chatting with EmoBot
        - End the session and optionally rate your post-chat mood

File Structure:
    - chat_bot.py - Main application logic and UI loop
    - profiles.json - Stores user profile data and chat history
    - /assets/ - Images, fonts, and audio used in the interface
    - button.py - Button class for handling clickable UI elements
    - chatbot.py - ChatBot class for generating responses
    - profile.py - Profile class for managing user profiles

Note:
    -  The ChatBot class appears to use an API key directly within the code
            consider securing this key and avoiding hardcoding for production use.
    - Profiles are limited to 3 slots by default in the current design.
    - Mood tracking is numerical (1-7 scale).