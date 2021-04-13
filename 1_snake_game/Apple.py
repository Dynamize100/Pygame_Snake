import pygame
from random import randint

DIR_RESOURCES = "resources/"
FILE_IMAGE_SPRITE_APPLE = DIR_RESOURCES + "appleFoodSm.png"

PROP_SIZE_BLOCK = 30
PROP_SIZE_SCREEN_WIDTH = 1000
PROP_SIZE_SCREEN_HEIGHT = 900
#PROP_SIZE_SCREEN_BORDER = 70

PROP_SCREEN_OFFSET = 10

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load(FILE_IMAGE_SPRITE_APPLE).convert_alpha()
        self.x = (randint(3, int(PROP_SIZE_SCREEN_WIDTH / PROP_SIZE_BLOCK) - 3) * PROP_SIZE_BLOCK)
        self.y = (randint(5, int(PROP_SIZE_SCREEN_HEIGHT / PROP_SIZE_BLOCK) - 3) * PROP_SIZE_BLOCK)+PROP_SCREEN_OFFSET

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = (randint(3, int(PROP_SIZE_SCREEN_WIDTH / PROP_SIZE_BLOCK) - 3) * PROP_SIZE_BLOCK)
        self.y = (randint(5, int(PROP_SIZE_SCREEN_HEIGHT / PROP_SIZE_BLOCK) - 3) * PROP_SIZE_BLOCK)+PROP_SCREEN_OFFSET