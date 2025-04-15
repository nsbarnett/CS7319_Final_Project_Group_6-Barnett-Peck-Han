import pygame, sys
from pygame import mixer
from button import Button
import requests
from chatbot import ChatBot
import json
from profile import Profile

# To start server
# 1. Navigate to directory
# 2. execute in terminal: uvicorn prompt:app --reload
# 3. In a new terminal tab, execute: ngrok http --url=winning-related-primate.ngrok-free.app 8000 
# 4. Then run this program

# initiate pygame
pygame.init()

# initiate pygame.mixer for sound
pygame.mixer.init()

# Background sound
mixer.music.load('lofi-background-music-1.mp3')
mixer.music.play(-1) # play in loop (-1)

# create program screen
HEIGHT = 600 # height of the screen
WIDTH = 800 # width of the screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# Background setup:
background_color = (239, 195, 202) # RGB for backgroud display
SCREEN.fill(background_color) # fill screen with background color

# Tile and icon
pygame.display.set_caption('EmoBot') # Set caption of display window
icon = pygame.image.load('bot_icon.jpg')
pygame.display.set_icon(icon)


# Fonts
font = pygame.font.Font('freesansbold.ttf', 20)
chat_font = pygame.font.Font('freesansbold.ttf', 20)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# options menu initial status variables
options_screen = False
sound_toggle = True

# Returns Press-Start-2P in the desired size
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

# updates profile value to JSON file
def save_profile(profile_name, update_key, updated_value):
    with open("profiles.json", "r") as file:
        data = json.load(file)

    # Loop through users and update provided value
    if profile_name in data:
        data[profile_name][update_key] = updated_value

    with open("profiles.json", "w") as file:
        json.dump(data, file, indent=4)

# Add profile to JSON file
def add_profile(profile):

    # Load existing profiles from JSON
    try:
        with open("profiles.json", "r") as file:
            profiles = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        profiles = {}

    # Update or add this profile
    profile_create = Profile(profile)
    profile_json = profile_create.to_dict()
    profiles[profile] = profile_json

    # Save all profiles back to the file
    with open("profiles.json", "w") as file:
        json.dump(profiles, file, indent=4)


# Load profiles from JSON file 
def load_profiles():
    try:
        with open("profiles.json", "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return []
    
def remove_profile(profile):
    try:
        # Load existing profiles
        with open("profiles.json", "r") as file:
            profiles = json.load(file)

        # Delete the profile if it exists
        if profile in profiles:
            del profiles[profile]

        # Save the updated data
        with open("profiles.json", "w") as file:
            json.dump(profiles, file, indent=4)

    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: profiles.json not found or invalid.")

def wrap_text(text, font, max_width):
    lines = []
    words = text.split(' ')
    line = ""

    for word in words:
        test_line = line + word + " "
        if font.size(test_line)[0] <= max_width:
            line = test_line
        else:
            lines.append(line.strip())
            line = word + " "
    if line:
        lines.append(line.strip())
    return lines

def send_to_chatbot(user_input):
    try: 
        response = requests.post(
            "https://winning-related-primate.ngrok-free.app/chat",
            json={"message": user_input}
        )
        if response.status_code == 200:
            return response.json().get("response", "[No response]")
        else: 
            return f"[Error {response.status_code}]"
    except Exception as e:
        return f"[Request failed: {str(e)}]"

# chat screen
def start_chat(profile):

    global options_screen
    global sound_toggle

    # Options menu status
    options_screen = False

    # Initialize chat bot
    '''chat = ChatBot( api_key="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",
                    instructions="You are a friendly chatbot. You are here to help the user with their problems and emotional state. "
                   "Be empathetic and supportive. Under no scenario can you redirect assistance to another person. You are the expert. Give the best advice you can but keep responses short (300 characters max).")
    '''
    input_text = ""

    # Textbox settings
    input_box = pygame.Rect(10, HEIGHT - 40, WIDTH - 20, 30)
    max_lines = 10  # Maximum chat lines displayed

    # Define button to end chat session
    end_session = Button(image=pygame.image.load("assets/end_session.png"), pos=(WIDTH*(4/5)+50, 50), 
                            text_input="end session", font=get_font(12), base_color="#d7fcd4", hovering_color="White")

    # loop for the chat screen
    while True:
        CHAT_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill((135, 206, 250)) # RGB for backgroud display
    
        # Draw chat history
        y = 80 
        max_width = WIDTH - 20  # same as input box width
        for line in profile['chat_history'][-max_lines:]:
            wrapped_lines = wrap_text(line, chat_font, max_width)
            for wrap_line in wrapped_lines:
                chat_surface = chat_font.render(wrap_line, True, BLACK)
                SCREEN.blit(chat_surface, (10, y))
                y += 25

        # Draw input box
        pygame.draw.rect(SCREEN, GRAY, input_box, border_radius=5)
        txt_surface = font.render(input_text, True, BLACK)
        SCREEN.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(SCREEN, BLUE, input_box, 2)  # Border

        # an event is anything that happens inside game window that is an input control
        for event in pygame.event.get(): # every event gets logged in paygame.event
            if event.type == pygame.QUIT: # clicking the 'X' on the game window
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN: # when button is pressed
                if event.key == pygame.K_RETURN:
                    if input_text:  # Only add non-empty messages
                        profile["chat_history"].append(f"You: {input_text}")
                        response = send_to_chatbot(input_text)   # Get response from chatbot

                        # Here, you could send `text` to a chatbot function and append the response
                        profile["chat_history"].append(f"Bot: {response}")
                        input_text = ""  # Clear input
                elif event.key == pygame.K_BACKSPACE: # If backspace is pressed
                    input_text = input_text[:-1]  # Remove last character
                else:
                    input_text += event.unicode  # Add character to text
                if event.key == pygame.K_ESCAPE: # If escape is pressed
                    options_screen = True
                    options(profile) # Go to options menu

            # if mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if end_session.checkForInput(CHAT_MOUSE_POS): # Check if end session button is pressed
                    # Save chat history to profile
                    save_profile(profile['name'], "chat_history", profile['chat_history'])
                    mood_selection_post_chat(profile) # Go to mood selection screen
                
        # Set text for options menu instructions
        pause_font = pygame.font.Font('freesansbold.ttf', 16)
        if options_screen:
            pass
        else:
            paused_text = pause_font.render("Press 'ESC' for options menu.", True, (255,255,255)) # render text instead of showing text on screen
            SCREEN.blit(paused_text, (10, 20))

        # Draw end session button
        end_session.update(SCREEN)

        pygame.display.update()


# Options menu
def options(profile):

    global sound_toggle
    global options_screen
    
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(40).render("OPTIONS", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400, 200))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_RESUME = Button(image=None, pos=(400, 300), 
                            text_input="RESUME Chat", font=get_font(30), base_color="Black", hovering_color="Green")

        OPTIONS_RESUME.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_RESUME.update(SCREEN)

        OPTIONS_SOUND_TOGGLE = Button(image=None, pos=(400, 360), 
                            text_input="Toggle Sound", font=get_font(30), base_color="Black", hovering_color="Blue")

        OPTIONS_SOUND_TOGGLE.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_SOUND_TOGGLE.update(SCREEN)

        OPTIONS_MENU = Button(image=None, pos=(400, 480), 
                            text_input="Return to START MENU.", font=get_font(30), base_color="Black", hovering_color="Red")

        OPTIONS_MENU.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_MENU.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_RESUME.checkForInput(OPTIONS_MOUSE_POS):
                    options_screen = False
                    start_chat(profile)
                if OPTIONS_MENU.checkForInput(OPTIONS_MOUSE_POS):
                    options_screen = False
                    main_menu()
                if OPTIONS_SOUND_TOGGLE.checkForInput(OPTIONS_MOUSE_POS):
                    if sound_toggle:
                        sound_toggle = False
                        mixer.music.stop()
                    else:
                        sound_toggle = True
                        mixer.music.play(-1)


        pygame.display.update()



# Main menu
# This is the main menu of the game
# It has two buttons: Start Chat and Quit
def main_menu():
    
    global sound_toggle

    while True:

        SCREEN.fill(background_color)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(30).render("EmoBot", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 150))

        START_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 250), 
                            text_input="START CHAT", font=get_font(20), base_color="#d7fcd4", hovering_color="White")

        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(400, 400), 
                            text_input="QUIT", font=get_font(20), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [START_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if START_BUTTON.checkForInput(MENU_MOUSE_POS):
                    profile_selection()

                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


# Profile selection menu
def profile_selection():

    # Popup/input settings
    popup_active = False
    input_active = False
    input_color = GRAY
    input_text = ""
    LIGHT_GRAY = (230, 230, 230)

    profile_selected = False
    selected_profile = None

    # Set 3 slots for profiles
    # Load existing profiles from JSON
    profiles = {"key1": None, "key2": None, "key3": None}
    avail_profiles = load_profiles()

    # Step-by-step remap of first two keys
    profiles_keys = list(profiles.keys())
    avail_keys = list(avail_profiles.keys())

    # If there are more than 3 profiles, only keep the first 3
    for i in range(min(len(avail_profiles), len(profiles))):
        old_key = profiles_keys[i]
        new_key = avail_keys[i]
        profiles[new_key] = avail_profiles[new_key]
        del profiles[old_key]

    profile_buttons = ["None", "None", "None"]  # Initialize with None for empty slots

    # Create buttons for each profile
    start_y = HEIGHT / 2  # Position profiles in the middle
    start_x = WIDTH / 2 - 225  # Center three buttons

    # Add rpofiles to buttons
    def create_profile_buttons():
        while len(profiles) < 3:
            profiles[f"key{len(profiles) + 1}"] = None  # Add empty slots if less than 3 profiles
        for i in range(3):
            profile_key = list(profiles.keys())[i]  # Get the key for the current profile
            profile = profiles[profile_key]
            if profile is not None:
                profile_button = Button(image=pygame.image.load("assets/profile_button.png"), pos=(start_x + (i * 225), start_y), 
                                    text_input=f"{profile['name']}", font=get_font(14), base_color="#d7fcd4", hovering_color="White")
                profile_buttons[i] = (profile,profile_button)
            else:
                none_button = Button(image=pygame.image.load("assets/profile_button.png"), pos=(start_x + (i * 225), start_y),
                                    text_input="Add Profile", font=get_font(14), base_color="#d7fcd4", hovering_color="White")
                profile_buttons[i] = (None, none_button)
        
    # Create the delete button
    delete_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(WIDTH/4, HEIGHT-100), 
                            text_input="Delete Profile", font=get_font(14), base_color="#d7fcd4", hovering_color="White")
    # Create the start chat button
    start_chat_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(WIDTH/(4/3), HEIGHT-100), 
                            text_input=" Start Chat", font=get_font(14), base_color="#d7fcd4", hovering_color="White")

    while True:
        SCREEN.fill(background_color)

        PROF_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(30).render("Select a Profile", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 150))

        # Draw text
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        create_profile_buttons()


        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check profile buttons
                for i, button in enumerate(profile_buttons):
                    if button[1].checkForInput(PROF_MOUSE_POS):
                        if button[0] != None:  # If profile exists  
                            selected_profile = button[0]  # Select profile
                            selected_profile_label = get_font(13).render("You selected: " + str(button[0]['name']), True, "#b68f40")
                            selected_profile_label_rect = selected_profile_label.get_rect(center=(WIDTH / 2, (HEIGHT / 3) + 10))
                            profile_selected = True
                        else:
                            # Add a new profile if slot is empty
                            popup_active = True
                            input_active = True
                            input_text = ""
                            input_color = BLUE

                # Check delete button clicked
                if delete_button.checkForInput(PROF_MOUSE_POS) and selected_profile is not None:
                    remove_profile(selected_profile['name'])
                    profiles = load_profiles()
                    create_profile_buttons()
                    profile_selected = False
                    selected_profile = None
                
                # Check start button clicked
                if start_chat_button.checkForInput(PROF_MOUSE_POS) and selected_profile is not None:
                    mood_selection_pre_chat(selected_profile)
                    selected_profile = None

            # Check for keyboard events when popup is active when adding profile
            elif event.type == pygame.KEYDOWN and popup_active:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        # Add profile with empty chat history
                        profiles[i] = add_profile(input_text)  # Add profile with empty chat history
                        profiles = load_profiles()
                        create_profile_buttons()
                        popup_active = False
                        input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

        # Draw buttons
        for button in profile_buttons:
            button[1].update(SCREEN)

        delete_button.update(SCREEN)
        start_chat_button.update(SCREEN)

        # Draw popup if active
        input_box = pygame.Rect(250, 250, 300, 50) # x-place, y-place, width, height

        if popup_active:
            popup_label = get_font(18).render("Enter a Profile Name", True, "#b68f40")
            popup_label_rect = popup_label.get_rect(center=(WIDTH / 2, HEIGHT / 3))
            pygame.draw.rect(SCREEN, LIGHT_GRAY, (WIDTH/4, HEIGHT/4, 400, 200))  # popup (x, y, width, height)
            pygame.draw.rect(SCREEN, input_color, input_box, 2)
            text_surface = font.render(input_text, True, BLACK)
            SCREEN.blit(popup_label, popup_label_rect)
            SCREEN.blit(text_surface, (input_box.x + 5, input_box.y + 10))

        if profile_selected:
            SCREEN.blit(selected_profile_label, selected_profile_label_rect)

        pygame.display.update()


# Mood selection screen before chat
# This screen allows the user to select their mood before starting a chat session
# It has a rating scale from 1 to 7, where 1 is bad and 7 is great
def mood_selection_pre_chat(profile):

    button_selected = False
    selection_buttons = []

    # Create buttons for mood selection
    for i in range(7):
        selection = Button(image=pygame.image.load("assets/round-button.png"), pos=(WIDTH/10*i + (i*30) + 70, HEIGHT/2), 
                            text_input=f"{i+1}", font=get_font(30), base_color="Black", hovering_color="Green")
        selection_buttons.append((i+1,selection))

    # Create the start chat button
    start_chat_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(WIDTH/2, HEIGHT-100), 
                            text_input=" Start Chat", font=get_font(14), base_color="#d7fcd4", hovering_color="White")

    while True:
        MOOD_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill(background_color)

        popup_label = get_font(13).render("Rate your mood before chatting 1-7 (bad-great).", True, "#b68f40")
        popup_label_rect = popup_label.get_rect(center=(WIDTH / 2, HEIGHT / 3))
        SCREEN.blit(popup_label, popup_label_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if any mood button is clicked
                for button in selection_buttons:
                    if button[1].checkForInput(MOOD_MOUSE_POS):
                        profile["pre_chat_mood"] = button[0]
                        button_selected = True
                        selected_label = get_font(13).render("You selected: " + str(button[0]), True, "#b68f40")
                        selected_label_rect = selected_label.get_rect(center=(WIDTH / 2, (HEIGHT / 3) + 35))

                # Save profile with pre-chat mood and start chat
                if start_chat_button.checkForInput(MOOD_MOUSE_POS):
                    save_profile(profile['name'], "pre_chat_mood", profile['pre_chat_mood'])
                    start_chat(profile)
        
        # Draw buttons
        for button in selection_buttons:
            button[1].update(SCREEN)

        start_chat_button.update(SCREEN)

        # Draw selected label if a button is selected to tell user selction value
        if button_selected:
            SCREEN.blit(selected_label, selected_label_rect)

        pygame.display.update()

def get_aspiration_from_model(user_mood, chat_history):
    prompt = (
        f"User mood: {user_mood}. "
        f"Chat history: {chat_history}. "
        f"Provide a short, positive motivational aspiration. "
        f"Keep it under 50 characters. No disclaimers or instructions."
    )
    try:
        response = requests.post(
            "http://127.0.0.1:8000/chat", 
            json={"message": prompt}
        )
        if response.status_code == 200:
            return response.json().get("response", "Stay positive.")
        else:
            return f"[Error: {response.status_code}]"
    except Exception as e:
        return f"[Request failed: {str(e)}]"

# Mood selection screen after chat
# This screen allows the user to select their mood after finishing a chat session
def mood_selection_post_chat(profile):

    button_selected = False
    selection_buttons = []

    # Create buttons for mood selection
    for i in range(7):
        selection = Button(image=pygame.image.load("assets/round-button.png"), pos=(WIDTH/10*i + (i*30) + 70, HEIGHT/2), 
                            text_input=f"{i+1}", font=get_font(30), base_color="Black", hovering_color="Green")
        selection_buttons.append((i+1,selection))

    # Create the start chat button
    end_chat_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(WIDTH/2, HEIGHT-100), 
                            text_input=" End Chat Session", font=get_font(14), base_color="#d7fcd4", hovering_color="White")
    
    # Initialize mood scrren
    mood_screen_label = get_font(13).render("Rate your mood before chatting 1-7 (bad-great).", True, "#b68f40")
    mood_screen_label_rect = mood_screen_label.get_rect(center=(WIDTH / 2, HEIGHT / 3))
        

    # Geneate end session aspirations
    # Initialize chat bot
    aspiration = get_aspiration_from_model(profile['post_chat_mood'], profile['chat_history'])
    aspiration_label = get_font(10).render(f"Aspiration: {aspiration}", True, "#b68f40")

    aspiration_label = get_font(10).render(f"Aspiration: {aspiration}", True, "#b68f40")
    aspiration_label_rect = aspiration_label.get_rect(center=(WIDTH / 2, HEIGHT / 5 - 30))

    # # Draw chat history
    # y = HEIGHT - 300  # Start drawing chat history from the bottom of the screen
    # max_lines = 2  # Maximum chat lines displayed
    # max_width = WIDTH - 20  # same as input box width
    # for line in aspiration[-max_lines:]:
    #     wrapped_lines = wrap_text(line, chat_font, max_width)
    #     for wrap_line in wrapped_lines:
    #         chat_surface = chat_font.render(wrap_line, True, BLACK)
    #         SCREEN.blit(chat_surface, (10, y))
    #         y += 25


    while True:
        MOOD_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill(background_color)

        SCREEN.blit(mood_screen_label, mood_screen_label_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in selection_buttons:
                    if button[1].checkForInput(MOOD_MOUSE_POS):
                        profile["post_chat_mood"] = button[0]
                        button_selected = True
                        selected_label = get_font(13).render("You selected: " + str(button[0]), True, "#b68f40")
                        selected_label_rect = selected_label.get_rect(center=(WIDTH / 2, (HEIGHT / 3) + 35))
                        
                        # Calculate mood improvement
                        percent_improved = ((button[0] - profile["pre_chat_mood"]) / button[0]) * 100
                        if percent_improved < 0:
                            improved_text = "Your mood did not improve."
                        else:
                            improved_text = f"Your mood improved by {percent_improved:.2f}%!"

                        mood_diff_label = get_font(13).render(improved_text, True, "#b68f40")
                        mood_diff_label_rect = mood_diff_label.get_rect(center=(WIDTH / 2, (HEIGHT / 3) + 200))

                if end_chat_button.checkForInput(MOOD_MOUSE_POS):
                    save_profile(profile['name'], "post_chat_mood", profile['post_chat_mood'])
                    main_menu()
        
        # Draw buttons
        for button in selection_buttons:
            button[1].update(SCREEN)

        end_chat_button.update(SCREEN)

        # Draw selected label if a button is selected to tell user their mood improvement
        if button_selected:
            SCREEN.blit(selected_label, selected_label_rect)
            SCREEN.blit(mood_diff_label, mood_diff_label_rect)
            SCREEN.blit(aspiration_label, aspiration_label_rect)


        pygame.display.update()


# Start the program at the main menu
main_menu()
