import pygame, json, random
from sys import exit as sysExit
#from keyboardListen import startListening
#from objPointer import Pointer
#from threading import Thread

'''pointer = Pointer("")  # Make a variable connected to parallel script
# Here we make a new thread with startListening from keyboardListen.py
# It's like say run startListening(pointer) in parallele
process = Thread(target=startListening, args=(pointer, ))
process.start()  # We start the Thread'''


def draw_line(string, font, color):
  '''Make a render object of a line of char'''
  text_to_render = font.render(string, True, color, None)
  return text_to_render


def draw_textBox_frame(string,
                       pos_x,
                       pos_y,
                       size=32,
                       font="default",
                       color=(0, 0, 0)):
  '''Draw one frame of a textBox'''
  if font == "default":  # If default is choose, the game load Ubuntu from herself for the font
    font = pygame.font.Font("static/RobotoMono-Regular.ttf", size)

  if string.find("\n") == -1:
    # There is no \n in the string
    text_to_render = draw_line(string, font, color)
    textBox = text_to_render.get_rect()
    textBox.center = pos_x, pos_y
    display_surface.blit(text_to_render, textBox)
  else:
    # There is \n in the string
    lines = string.split("\n")
    lines_to_render = []
    for i in range(len(lines)):
      # Making the pygame render object for all lines
      lines_to_render.append(draw_line(lines[i], font, color))
    for i in range(len(lines_to_render)):
      # Adding all render object to the screen with a step in y coord
      lineBox = lines_to_render[i].get_rect()
      lineBox.center = pos_x, pos_y + 30 * i
      display_surface.blit(lines_to_render[i], lineBox)


def get_random_quote():
  # Cette fonction a été générer par GPT-3.5
  # Je n'ai pas eu le temps de la coder moi-même

  # Charger le fichier JSON
  with open("static/french.json", 'r', encoding='utf-8') as file:
    content = json.load(file)

  # Choisir aléatoirement un groupe
  group = random.choice(content['groups'])

  # Choisir aléatoirement une citation dans le groupe sélectionné
  quote_id = random.randint(group[0], group[1])
  quote = next((q for q in content['quotes'] if q['id'] == quote_id), None)

  if quote:
    # Diviser la citation en mots
    words = quote['text'].split()
    return words
  else:
    return ["écrivez"]


# Pygame window start
pygame.init()
display_surface = pygame.display.set_mode((800, 400))
display_surface.fill((255, 255, 255))
gameIsRunning = True  # I like say this more than just True in my while
wordToWrite = ""  # Word who the player need to write
words = []  # The list of words than the player will write
# For center to the bottom the text
textBox_x = display_surface.get_width() / 2
textBox_y = display_surface.get_height() - 20
'''while gameIsRunning == True :
    userInput = pointer.get_var() # We intercept this variable from the other parallel execution -
    display_surface.fill((255, 255, 255)) # We clear the display surface
    # If the player wrote the word to write
    if userInput == wordToWrite :
        try :
            if words.index(wordToWrite) != len(words) : # While citation have other words in
                del words[0] # Del the first of the list
                pointer.set_var("")
                userInput = ""
                wordToWrite = words[0] # Pass to the next
            else : # Citation is complete
                words = get_random_quote() # Get a new quote
                wordToWrite = words[0] # Get the first word to print
        except Exception :
            # We start here when wordToWrite == ''
            words = get_random_quote()
            wordToWrite = words[0]
    # Print the text to write
    draw_textBox_frame(wordToWrite, textBox_x, textBox_y, size=16, color=(128, 128, 128))
    # Print on the other text the text already write by the user
    draw_textBox_frame(userInput, textBox_x, textBox_y, size=16)
    
    for event in pygame.event.get():
        # When the execution is killed
        if event.type == pygame.QUIT:
            # Stop all the loop
            pointer.kill_script() # Kill the thread
            pygame.quit() # Quit pygame
            sysExit() # Kill this script
            
    pygame.display.update() # Updating the game frame per frame'''
