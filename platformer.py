# Dino player images by Arks
# https://arks.itch.io/dino-characters
# Twitter: @ScissorMarks

# Chicken leg png from:
# https://www.pngfind.com/download/xJoooi_chicken-leg-xbox-a-button-pixel-hd-png/

# Spike monster by bevouliin.com
# https://opengameart.org/content/bevouliin-free-ingame-items-spike-monsters

# All SFX and BGM sounds from freesound.org
# https://freesound.org/

import pygame
import engine

def drawText(string, x, y):
  text = font.render(string, True, MUSTARD, DARK_GREY)
  text_rect = text.get_rect()
  text_rect.topleft = (x, y)
  screen.blit(text, text_rect)

def playSfx(file_path, volume):
  sfx = pygame.mixer.Sound(file_path)
  sfx.set_volume(volume)
  sfx.play()

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
player_state = 'idle' # or 'walking'

player_animations = {
  'idle': engine.Animation([
    pygame.image.load('assets/vita/vita_00.png'),
    pygame.image.load('assets/vita/vita_01.png'),
    pygame.image.load('assets/vita/vita_02.png'),
    pygame.image.load('assets/vita/vita_03.png')
  ]),
  'walking': engine.Animation([
    pygame.image.load('assets/vita/vita_04.png'),
    pygame.image.load('assets/vita/vita_05.png'),
    pygame.image.load('assets/vita/vita_06.png'),
    pygame.image.load('assets/vita/vita_07.png'),
    pygame.image.load('assets/vita/vita_08.png'),
    pygame.image.load('assets/vita/vita_09.png')
  ]),
  'jumping': engine.Animation([
    pygame.image.load('assets/vita/vita_11.png')
  ])
}

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
chicken_leg = pygame.image.load('assets/collectables/chicken-leg/chicken_leg_0.png')
collectable_animation = engine.Animation([
  pygame.image.load('assets/collectables/chicken-leg/chicken_leg_0.png'),
  pygame.image.load('assets/collectables/chicken-leg/chicken_leg_1.png'),
  pygame.image.load('assets/collectables/chicken-leg/chicken_leg_2.png'),
  pygame.image.load('assets/collectables/chicken-leg/chicken_leg_3.png')
])
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
pygame.mixer.music.set_volume(0.15)
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

  # ---------- #
  #   UPDATE   #
  # ---------- #
  
  if game_state == 'playing':
    # update collectables animation
    collectable_animation.update()

    # update player animations
    player_animations[player_state].update()

    new_player_x = player_x
    new_player_y = player_y

    # player input
    keys = pygame.key.get_pressed()
    # left
    if keys[pygame.K_LEFT]:
      new_player_x -= 2
      player_direction = 'left'
      if player_on_ground:
        player_state = 'walking'
    # right
    if keys[pygame.K_RIGHT]:
      new_player_x += 2
      player_direction = 'right'
      if player_on_ground:
        player_state = 'walking'
    # jump
    if keys[pygame.K_SPACE] and player_on_ground:
      player_speed = -5
      player_state = 'jumping'
      playSfx('assets/sfx/jump.wav', 0.4)
    # idle
    if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_SPACE]:
      player_state = 'idle'

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
        playSfx('assets/sfx/collect.wav', 0.5)
        collectables.remove(c)
        score += 1
        # changing game_state to win
        if score >= 2:
          playSfx('assets/sfx/stage-clear.wav', 0.2)
          game_state = 'win'

    # see if any enemy hit
    for e in enemies:
      if e.colliderect(player_rect):
        playSfx('assets/sfx/hurt.wav', 0.2)
        lives -= 1
        # reset player position
        player_x = 300
        player_y = 0
        player_speed = 0
        # changing game_state to lose
        if lives <= 0:
          playSfx('assets/sfx/game-over.wav', 0.2)
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
    collectable_animation.draw(screen, c.x, c.y, False, False)

  # enemies
  for e in enemies:
    screen.blit(enemy_image, (e.x, e.y))

  # player
  if player_direction == 'left':
    player_animations[player_state].draw(screen, player_x, player_y, True, False)
  else :
    player_animations[player_state].draw(screen, player_x, player_y, False, False)

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
  if game_state != 'playing':
    pygame.mixer.music.stop()

  #present screen
  pygame.display.flip()

  clock.tick(60)

# quit
pygame.quit()