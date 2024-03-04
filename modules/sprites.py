import pygame
import random
from pygame.locals import *
from sys import exit
from typing.objPointer import Pointer
from typing.text_gui_output import *
from typing.keyboardListen import startListening
from threading import Thread
# Initialisation de Pygame
pygame.init()

# Création de la fenêtre de jeu
screen = pygame.display.set_mode((400, 300), RESIZABLE)
pygame.display.set_caption("Test de déplacement du joueur")


# Charger les sprites du héros
def cut_hero_sprites(sheet_path, rows, columns):
  """
    Fonction pour découper les sprites du héros à partir d'une feuille de sprite.

    Args:
        sheet_path (str): Le chemin vers la feuille de sprite du héros.
        rows (int): Le nombre de lignes dans la feuille de sprite.
        columns (int): Le nombre de colonnes dans la feuille de sprite.

    Returns:
        list: Une liste des sprites découpés.
    """
  sheet = pygame.image.load(sheet_path).convert_alpha()
  sheet_width, sheet_height = sheet.get_size()
  cell_width = sheet_width // columns
  cell_height = sheet_height // rows
  sprites = []
  for row in range(rows):
    for col in range(columns):
      x = col * cell_width
      y = row * cell_height
      sprite = sheet.subsurface((x, y, cell_width, cell_height))
      sprites.append(sprite)
  return sprites


hero_sprites = cut_hero_sprites("static/sheet.png", 8, 4)

# Définition des indices pour chaque direction du héros
direction_indices = {
    "bas": 0,
    "diagonal_bas_gauche": 1,
    "gauche": 2,
    "diagonal_haut_gauche": 3,
    "haut": 4,
    "diagonal_haut_droite": 5,
    "droite": 6,
    "diagonal_bas_droite": 7
}

# Position initiale du joueur et vitesse de déplacement
x, y = 100, 150
move_speed = 5

# Initialisation de l'horloge de Pygame
clock = pygame.time.Clock()

# Variable pour la boucle principale
running = True

# Index de l'animation du héros
frame_index = 0

# Nombre de frames par direction du héros
frame_count = len(hero_sprites) // len(direction_indices)

# Direction initiale du héros
current_direction = "bas"


# Charger les sprites des ennemis (carré et cercle)
def load_enemy_sprites():
  """
    Fonction pour charger les sprites des ennemis (carré et cercle).

    Returns:
        list: Une liste des sprites des ennemis.
    """
  shapes = ["square", "circle"]
  sprites = []
  for shape in shapes:
    size = random.randint(20, 40)  # Taille aléatoire pour les formes
    if shape == "circle":
      sprite = pygame.Surface((size, size), pygame.SRCALPHA)
      pygame.draw.circle(sprite, (255, 0, 0), (size // 2, size // 2),
                         size // 2)
    elif shape == "square":
      sprite = pygame.Surface((size, size), pygame.SRCALPHA)
      pygame.draw.rect(sprite, (255, 0, 0), (0, 0, size, size))
    sprites.append(sprite)
  return sprites


enemy_sprites = load_enemy_sprites()


# Fonction pour faire apparaître un ennemi aléatoirement sur un côté de l'écran
def spawn_enemy():
  """
    Fonction pour faire apparaître un ennemi aléatoirement sur un côté de l'écran.

    Returns:
        tuple: Les coordonnées x, y et la direction de l'ennemi.
    """
  side = random.choice(["top", "bottom", "left", "right"])
  if side == "top":
    x = random.randint(0, screen.get_width() - enemy_sprites[0].get_width())
    y = -enemy_sprites[0].get_height()
    direction = (0, 1)  # Vers le bas

  elif side == "bottom":
    x = random.randint(0, screen.get_width() - enemy_sprites[0].get_width())
    y = screen.get_height()
    direction = (0, -1)  # Vers le haut
  elif side == "left":
    x = -enemy_sprites[0].get_width()
    y = random.randint(0, screen.get_height() - enemy_sprites[0].get_height())
    direction = (1, 0)  # Vers la droite
  elif side == "right":
    x = screen.get_width()
    y = random.randint(0, screen.get_height() - enemy_sprites[0].get_height())
    direction = (-1, 0)  # Vers la gauche
  return x, y, direction


# Initialisation des ennemis
enemies = []

# Seuil de nombre maximal d'ennemis
max_enemies = 5

# Init for text gui
gameIsRunning = True  # I like say this more than just True in my while
wordToWrite = ""  # Word who the player need to write
words = []  # The list of words than the player will write
# For center to the bottom the text
textBox_x = screen.get_width() / 2
textBox_y = screen.get_height() - 20

pointer = Pointer("")  # Make a variable connected to parallel script
# Here we make a new thread with startListening from keyboardListen.py
# It's like say run startListening(pointer) in parallele
process = Thread(target=startListening, args=(pointer, ))
process.start()  # We start the Thread

print("Ne touchez pas les cubes Rouges ! Ce sont des ennemies, pour les survivre, écrivez ce qui il y afficher en bas !")
# Boucle principale
while running:
  userInput = pointer.get_var(
  )  # We intercept this variable from the other parallel execution -
  screen.fill((0, 0, 0))  # We clear the display surface
  # If the player wrote the word to write
  if userInput == wordToWrite:
    try:
      if words.index(wordToWrite) != len(
          words):  # While citation have other words in
        del words[0]  # Del the first of the list
        pointer.set_var("")
        userInput = ""
        wordToWrite = words[0]  # Pass to the next
      else:  # Citation is complete
        words = get_random_quote()  # Get a new quote
        wordToWrite = words[0]  # Get the first word to print
    except Exception:
      # We start here when wordToWrite == ''
      words = get_random_quote()
      wordToWrite = words[0]
  # Print the text to write
  draw_textBox_frame(wordToWrite,
                     textBox_x,
                     textBox_y,
                     size=16,
                     color=(150, 150, 150))
  # Print on the other text the text already write by the user
  draw_textBox_frame(userInput, textBox_x, textBox_y, size=16, color=(255, 255, 255))


  # Gérer les événements
  keys = pygame.key.get_pressed()
  for event in pygame.event.get():
    if event.type == QUIT:
      running = False

  # Détection du mouvement du joueur
  if keys[K_LEFT]:
    if keys[K_UP]:
      # Diagonale haut gauche
      current_direction = "diagonal_haut_gauche"
      x -= move_speed
      y -= move_speed
    elif keys[K_DOWN]:
      # Diagonale bas gauche
      current_direction = "diagonal_bas_gauche"
      x -= move_speed
      y += move_speed
    else:
      # Mouvement gauche
      current_direction = "gauche"
      x -= move_speed
  elif keys[K_RIGHT]:
    if keys[K_UP]:
      # Diagonale haut droite
      current_direction = "diagonal_haut_droite"
      x += move_speed
      y -= move_speed
    elif keys[K_DOWN]:
      # Diagonale bas droite
      current_direction = "diagonal_bas_droite"
      x += move_speed
      y += move_speed
    else:
      # Mouvement droite
      current_direction = "droite"
      x += move_speed
  elif keys[K_UP]:
    # Mouvement haut
    current_direction = "haut"
    y -= move_speed
  elif keys[K_DOWN]:
    # Mouvement bas
    current_direction = "bas"
    y += move_speed

  # Affichage du joueur
  direction_index = direction_indices[current_direction]
  sprite_index = direction_index * frame_count + frame_index
  screen.blit(hero_sprites[sprite_index], (x, y))

  # Mettre à jour l'index de l'animation du joueur
  frame_index = (frame_index + 1) % frame_count

  # Limiter le nombre d'ennemis actifs
  if len(enemies) < max_enemies and random.random() < 0.01:
    enemy_x, enemy_y, enemy_direction = spawn_enemy()
    enemies.append({
        "x":
        enemy_x,
        "y":
        enemy_y,
        "direction":
        enemy_direction,
        "hitbox":
        pygame.Rect(enemy_x, enemy_y, enemy_sprites[0].get_width(),
                    enemy_sprites[0].get_height())
    })

  # Déplacer et afficher les ennemis
  for enemy in enemies:
    dx = x - enemy["x"]
    dy = y - enemy["y"]
    distance = max(1, ((dx**2) +
                       (dy**2))**0.5)  # Distance entre le héros et l'ennemi
    speed = 2  # Vitesse d'attraction
    enemy["x"] += (dx / distance) * speed
    enemy["y"] += (dy / distance) * speed
    screen.blit(enemy_sprites[0], (enemy["x"], enemy["y"]))
    enemy["hitbox"] = pygame.Rect(enemy["x"], enemy["y"],
                                  enemy_sprites[0].get_width(),
                                  enemy_sprites[0].get_height())

  # Vérifier les collisions avec les ennemis
  for enemy in enemies:
    if pygame.Rect(x, y, hero_sprites[0].get_width(),
                   hero_sprites[0].get_height()).colliderect(enemy["hitbox"]):
      # Collision détectée, fin du jeu
      running = False

  # Rafraîchir l'affichage
  pygame.display.update()
  clock.tick(30)

# Fermeture de Pygame et sortie du programme
pygame.quit()
exit()
