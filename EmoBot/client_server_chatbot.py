import pygame, sys
from pygame import mixer
from button import Button
from chatbot import ChatBot
import json
from profile import Profile

# initiate pygame
pygame.init()

# initiate pygame.mixer for sound
pygame.mixer.init()

# Background sound
mixer.music.load('lofi-background-music-1.mp3')
mixer.music.play(-1) # play in loop (-1)


# create game screen
HEIGHT = 600 # height of the screen
WIDTH = 800 # width of the screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT)) # (width, height)

# Background
# background_color = (113, 174, 177)
background_color = (239, 195, 202) # RGB for backgroud display
# BACKGROUND = pygame.image.load('4262432.jpg')
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

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

SCREEN.fill((135, 206, 250)) # RGB for backgroud display

# # List of profiles
# profiles = []

# Save all profiles to JSON file
def save_profiles(profiles):
    with open("profiles.json", "w") as file:
        json.dump(profiles, file, indent=4)


# Add profile to JSON file
def add_profile(profile):

    # Step 1: Load existing profiles from JSON
    try:
        with open("profiles.json", "r") as file:
            profiles = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        profiles = {}

    # Step 2: Update or add this profile
    profile_create = Profile(profile)
    profile_json = profile_create.to_dict()
    profiles[profile] = profile_json

    # Step 3: Save all profiles back to the file
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
        # Step 1: Load existing profiles
        with open("profiles.json", "r") as file:
            profiles = json.load(file)

        # Step 2: Delete the profile if it exists
        if profile in profiles:
            del profiles[profile]

        # Step 3: Save the updated data
        with open("profiles.json", "w") as file:
            json.dump(profiles, file, indent=4)

    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: profiles.json not found or invalid.")

# game loop
def start_chat(profile):

    # popup_active = True
    # selection_buttons = []

    # for i in range(7):
    #     SELECTION = Button(image=pygame.image.load("assets/round-button.png"), pos=(WIDTH/10*i + (i*30) + 70, HEIGHT/2), 
    #                         text_input=f"{i+1}", font=get_font(30), base_color="Black", hovering_color="Green")
    #     selection_buttons.append((i,SELECTION))

    # chat = ChatBot("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")
    input_text = ""

    # Textbox settings
    input_box = pygame.Rect(10, HEIGHT - 40, WIDTH - 20, 30)
    max_lines = 10  # Maximum chat lines displayed

    CHAT_MOUSE_POS = pygame.mouse.get_pos()

    global options_screen
    global sound_toggle

    # if sound_toggle:
    # # Background sound
    #     mixer.music.load('lofi-background-music-1.mp3')
    #     mixer.music.play(-1) # play in loop (-1)

    while True:
        SCREEN.fill((135, 206, 250)) # RGB for backgroud display
        
        # for button in selection_buttons:
        #     if button[1].checkForInput(PLAY_MOUSE_POS):
        #         profile["mood"] = button[0]
        #         print(profile["mood"])
        #         popup_active = False

        # Draw chat history
        y = 80 
        for line in profile['chat_history'][-max_lines:]:  # Show only the last `max_lines` messages
            chat_surface = chat_font.render(line, True, BLACK)
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

                        ##### CHANGE: CLIENT-SERVER CHATBOT #####
                        response = chat.get_response(input_text)  # Get response from chatbot

                        # Here, you could send `text` to a chatbot function and append the response
                        profile["chat_history"].append(f"Bot: {response}")
                        input_text = ""  # Clear input
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]  # Remove last character
                else:
                    input_text += event.unicode  # Add character to text
                if options_screen:
                    pass
                if event.key == pygame.K_ESCAPE:
                    options_screen = True
                    options(profile)


        pause_font = pygame.font.Font('freesansbold.ttf', 16)
        if options_screen:
            # mixer.music.stop()
            resume_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 150), 
                            text_input="RESUME", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
            if resume_button.checkForInput(CHAT_MOUSE_POS):
                options_screen = False

        else:
            paused_text = pause_font.render("Press 'ESC' for options menu.", True, (255,255,255)) # render text instead of showing text on screen
            SCREEN.blit(paused_text, (10, 20))

        # if popup_active:
        #     popup_label = get_font(18).render("Rate you mood 1-7 (bad-good)", True, "#b68f40")
        #     popup_label_rect = popup_label.get_rect(center=(WIDTH / 2, HEIGHT / 3))
        #     pygame.draw.rect(SCREEN, WHITE, ((WIDTH/4)-180, (HEIGHT/4)+20, 760, 200))  # popup (x, y, width, height)
        #     SCREEN.blit(popup_label, popup_label_rect)
        #     for button in selection_buttons:
        #         button[1].update(SCREEN)

        pygame.display.update()
        
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

def profile_selection():

    # Popup/input settings
    popup_active = False
    input_active = False
    input_color = GRAY
    input_text = ""
    LIGHT_GRAY = (230, 230, 230)

    selected_profile = None

    profiles = {"key1": None, "key2": None, "key3": None}
    avail_profiles = load_profiles()

    # Step-by-step remap of first two keys
    profiles_keys = list(profiles.keys())
    avail_keys = list(avail_profiles.keys())


    for i in range(min(len(avail_profiles), len(profiles))):
        old_key = profiles_keys[i]
        new_key = avail_keys[i]
        profiles[new_key] = avail_profiles[new_key]
        del profiles[old_key]

    profile_buttons = ["None", "None", "None"]  # Initialize with None for empty slots

    # Create buttons for each profile
    start_y = HEIGHT / 2  # Position profiles in the middle
    start_x = WIDTH / 2 - 225  # Center three buttons

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
                            print(selected_profile)
                            # button[1].changeColor(PROF_MOUSE_POS)
                            # start_chat(button[0])
                        else:
                            # Add a new profile if slot is empty
                            popup_active = True
                            input_active = True
                            input_text = ""
                            input_color = BLUE

                # Check delete button
                if delete_button.checkForInput(PROF_MOUSE_POS) and selected_profile is not None:
                    remove_profile(selected_profile['name'])
                    profiles = load_profiles()
                    create_profile_buttons()
                    selected_profile = None
                
                if start_chat_button.checkForInput(PROF_MOUSE_POS) and selected_profile is not None:
                    start_chat(selected_profile)
                    selected_profile = None

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
            # print(button)
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

        pygame.display.update()

def mood_selection(profile):

    MOOD_MOUSE_POS = pygame.mouse.get_pos()

    selection_buttons = []

    for i in range(7):
        SELECTION = Button(image=pygame.image.load("assets/round-button.png"), pos=(WIDTH/10*i + (i*30) + 70, HEIGHT/2), 
                            text_input=f"{i+1}", font=get_font(30), base_color="Black", hovering_color="Green")
        selection_buttons.append((i,SELECTION))

    button_check = selection_buttons[0]
    print(button_check, button_check[1])

    while True:
        SCREEN.fill(background_color)

        popup_label = get_font(13).render("Rate your mood before chatting 1-7 (bad-great).", True, "#b68f40")
        popup_label_rect = popup_label.get_rect(center=(WIDTH / 2, HEIGHT / 3))
        pygame.draw.rect(SCREEN, WHITE, ((WIDTH/4)-180, (HEIGHT/4)+20, 760, 200))  # popup (x, y, width, height)
        SCREEN.blit(popup_label, popup_label_rect)
        for button in selection_buttons:
            button[1].update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_check[1].checkForInput(MOOD_MOUSE_POS):
                    print('worked')
                # for button in selection_buttons:
                #     if button[1].checkForInput(MOOD_MOUSE_POS):
                #         print(button[0])
                        # profile["moods"].append(button[0])
                        # print(profile["moods"])
                        # popup_active = False

        pygame.display.update()





main_menu()