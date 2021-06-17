# Dino player images by Arks
# https://arks.itch.io/dino-characters
# Twitter: @ScissorMarks

# Chicken leg png from:
# https://www.pngfind.com/download/xJoooi_chicken-leg-xbox-a-button-pixel-hd-png/

# Spike monster by bevouliin.com
# https://opengameart.org/content/bevouliin-free-ingame-items-spike-monsters

import pygame

def drawText(string, x, y):
  text = font.render(string, True, MUSTARD, DARK_GREY)
  text_rect = text.get_rect()
  text_rect.topleft = (x, y)
  screen.blit(text, text_rect)

# constant variables
SCREEN_SIZE = (700,500)
DARK_GREY = (50,50,50)
MUSTARD = (205, 150, 20)

# init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Janebro\'s Platform Game')
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 24)

# game_states = playing // win // lose
game_state = 'playing'

# player
player_image = pygame.image.load('assets/vita/vita_00.png')
player_width = player_image.get_width()
player_height = player_image.get_height()
player_x = 300
player_y = 0
player_speed = 0
player_acceleration = 0.2
player_direction = 'right'

# platforms
platforms = [
  # middle
  pygame.Rect(100,300, 400, 50),
  # left
  pygame.Rect(100,250, 50, 50),
  # right
  pygame.Rect(450,250, 50, 50)
]

# collectables
chicken_leg = pygame.image.load('assets/collectables/chicken.png')
collectables = [
  pygame.Rect(100,200, 30, 30),
  pygame.Rect(200,250, 30, 30)
]

score = 0

# enemies
enemy_image = pygame.image.load('assets/enemies/spike_monster.png')
enemies = [
  pygame.Rect(150, 274, 35, 25)
]

lives = 3
lives_image = pygame.image.load('assets/vita/vita_00.png')
lives_image = pygame.transform.scale(lives_image, (player_image.get_width() - 15, player_image.get_height() - 15))

# ------- #
#   BGM   #
# ------- #

# Starting the mixer
pygame.mixer.init()
# Loading the song
pygame.mixer.music.load('assets/bgm/quest.mp3')
# Setting the volume
pygame.mixer.music.set_volume(0.2)
# Start playing the song looping forever
#pygame.mixer.music.play(-1)

running = True

while running:
# game loop

  # --------- #
  #   INPUT   #
  # --------- #

  # check for quit
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
  
  if game_state == 'playing':
    new_player_x = player_x
    new_player_y = player_y

    # player input
    keys = pygame.key.get_pressed()
    # left
    if keys[pygame.K_LEFT]:
      new_player_x -= 2
      player_direction = 'left'
    # right
    if keys[pygame.K_RIGHT]:
      new_player_x += 2
      player_direction = 'right'
    # if on the ground
    if keys[pygame.K_SPACE] and player_on_ground:
      player_speed = -5
      # jump sound
      jump_sfx = pygame.mixer.Sound('assets/sfx/jump.wav')
      jump_sfx.set_volume(0.4)
      jump_sfx.play()

    # ---------- #
    #   UPDATE   #
    # ---------- #

    # horizontal movement

    new_player_rect = pygame.Rect(new_player_x, player_y, player_width, player_height)
    x_collision = False

    # ... check against every platform
    for p in platforms:
      if p.colliderect(new_player_rect):
        x_collision = True
        break

    if x_collision == False:
      player_x = new_player_x

    # vertical movement

    player_speed += player_acceleration
    new_player_y += player_speed

    new_player_rect = pygame.Rect(player_x, new_player_y, player_width, player_height)
    y_collision = False
    player_on_ground = False

    # ... check against every platform
    for p in platforms:
      if p.colliderect(new_player_rect):
        y_collision = True
        player_speed = 0
        # if the platform is below the player
        if p[1] > new_player_y:
          # stick the player to the platform
          player_y = p[1] - player_height
          player_on_ground = True
        break

    if y_collision == False:
      player_y = new_player_y

    # see if any items have been collected
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for c in collectables:
      if c.colliderect(player_rect):
        pick_sfx = pygame.mixer.Sound('assets/sfx/collect.wav')
        pick_sfx.set_volume(0.5)
        pick_sfx.play()
        collectables.remove(c)
        score += 1
        # changing game_state to win
        if score >= 2:
          game_state = 'win'


    # see if any enemy hit
    for e in enemies:
      if e.colliderect(player_rect):
        pick_sfx = pygame.mixer.Sound('assets/sfx/hurt.wav')
        pick_sfx.set_volume(0.1)
        pick_sfx.play()
        lives -= 1
        # reset player position
        player_x = 300
        player_y = 0
        player_speed = 0
        # changing game_state to lose
        if lives <= 0:
          game_state = 'lose'

  # -------- #
  #   DRAW   #
  # -------- #

  # background
  screen.fill(DARK_GREY)

  # platforms
  for p in platforms:
    pygame.draw.rect(screen, MUSTARD, p)

  # collectables
  for c in collectables:
    screen.blit(chicken_leg, (c.x, c.y))

  # enemies
  for e in enemies:
    screen.blit(enemy_image, (e.x, e.y))

  # player
  if player_direction == 'right':
    screen.blit(player_image, (player_x, player_y))
  elif player_direction == 'left':
    screen.blit(pygame.transform.flip(player_image, True, False), (player_x, player_y))

  # HUD

  # score
  screen.blit(chicken_leg, (10, 10))
  drawText(str(score) , 45, 15)

  # lives
  for l in range(lives):
    screen.blit(lives_image, (600 + (l*30), 10))

  if game_state == 'win':
    drawText('YOU WIN!', 100, 100)
  if game_state == 'lose':
    drawText('YOU LOSE!', 100, 100)

  #present screen
  pygame.display.flip()

  clock.tick(60)

# quit
pygame.quit()