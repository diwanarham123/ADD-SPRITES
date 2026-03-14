import pygame
import random

pygame.init()

SPRITE_COLOR_CHANGE_EVENT = pygame.USEREVENT + 1
BACKGROUND_COLOR_CHANGE_EVENT = pygame.USEREVENT + 2

BLUE = pygame.Color('blue')
LIGHTBLUE = pygame.Color('lightblue')
DARKBLUE = pygame.Color('darkblue')
YELLOW = pygame.Color('yellow')
MAGENTA = pygame.Color('magenta')
ORANGE = pygame.Color('orange')
WHITE = pygame.Color('white')
GREEN = pygame.Color('green')
RED = pygame.Color('red')

class AutonomousSprite(pygame.sprite.Sprite):
  def __init__(self, color, height, width, screen_width, screen_height):
    super().__init__()
    self.image = pygame.Surface([width, height])
    self.image.fill(color)
    self.rect = self.image.get_rect()
    self.velocity = [random.choice([-1, 1]), random.choice([-1, 1])]
    self.screen_width = screen_width
    self.screen_height = screen_height

  def update(self):
    self.rect.move_ip(self.velocity)
    boundary_hit = False
    if self.rect.left <= 0 or self.rect.right >= self.screen_width:
      self.velocity[0] = -self.velocity[0]
      boundary_hit = True
    if self.rect.top <= 0 or self.rect.bottom >= self.screen_height:
      self.velocity[1] = -self.velocity[1]
      boundary_hit = True
    if boundary_hit:
      pygame.event.post(pygame.event.Event(SPRITE_COLOR_CHANGE_EVENT, sprite=self))
      pygame.event.post(pygame.event.Event(BACKGROUND_COLOR_CHANGE_EVENT))

  def change_color(self):
    new_color = random.choice([YELLOW, MAGENTA, ORANGE, WHITE])
    self.image.fill(new_color)
    print(f"Autonomous Sprite color changed to: {new_color}")

class PlayerSprite(pygame.sprite.Sprite):
  def __init__(self, color, height, width, screen_width, screen_height, speed):
    super().__init__()
    self.image = pygame.Surface([width, height])
    self.image.fill(color)
    self.rect = self.image.get_rect()
    self.speed = speed
    self.screen_width = screen_width
    self.screen_height = screen_height

  def update(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
      self.rect.x -= self.speed
    if keys[pygame.K_RIGHT]:
      self.rect.x += self.speed
    if keys[pygame.K_UP]:
      self.rect.y -= self.speed
    if keys[pygame.K_DOWN]:
      self.rect.y += self.speed

    self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))
    self.rect.y = max(0, min(self.rect.y, self.screen_height - self.rect.height))

def change_background_color():
  global bg_color
  new_bg_color = random.choice([BLUE, LIGHTBLUE, DARKBLUE])
  bg_color = new_bg_color
  print(f"Background color changed to: {new_bg_color}")


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Two Sprites Game")

all_sprites_list = pygame.sprite.Group()

player_sprite = PlayerSprite(RED, 40, 40, SCREEN_WIDTH, SCREEN_HEIGHT, 3)
player_sprite.rect.x = (SCREEN_WIDTH // 2) - 20
player_sprite.rect.y = (SCREEN_HEIGHT // 2) - 20
all_sprites_list.add(player_sprite)

autonomous_sprite = AutonomousSprite(GREEN, 30, 30, SCREEN_WIDTH, SCREEN_HEIGHT)
autonomous_sprite.rect.x = random.randint(0, SCREEN_WIDTH - 30)
autonomous_sprite.rect.y = random.randint(0, SCREEN_HEIGHT - 30)
all_sprites_list.add(autonomous_sprite)

bg_color = BLUE
screen.fill(bg_color)

exit_game = False
clock = pygame.time.Clock()

while not exit_game:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      exit_game = True
    elif event.type == SPRITE_COLOR_CHANGE_EVENT:
      if event.sprite == autonomous_sprite:
        autonomous_sprite.change_color()
    elif event.type == BACKGROUND_COLOR_CHANGE_EVENT:
      change_background_color()

  all_sprites_list.update()

  screen.fill(bg_color)
  all_sprites_list.draw(screen)

  pygame.display.flip()

  clock.tick(60)

pygame.quit()