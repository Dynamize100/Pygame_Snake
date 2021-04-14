import pygame


DIR_RESOURCES = "resources/"
FILE_IMAGE_SPRITE_HEAD = DIR_RESOURCES + "snakeHeadSm.png"

PROP_SIZE_BLOCK = 30
PROP_SIZE_SCREEN_WIDTH = 1000
PROP_SIZE_SCREEN_HEIGHT = 800

PROP_COORDINATES_X = 0
PROP_COORDINATES_Y = 1

PROP_ORIENTATION_SOUTH = 0
#PROP_ORIENTATION_WEST = 1
#PROP_ORIENTATION_NORTH = 2
#PROP_ORIENTATION_EAST = 3

PROP_ROTATION_STEP = 90

class SnakeHead:
    def __init__(self, parent_screen, position):
        self.parent_screen = parent_screen
        self.orientation = PROP_ORIENTATION_SOUTH
        self.prev_orientation = self.orientation
        self.snake_head_init = pygame.image.load(FILE_IMAGE_SPRITE_HEAD).convert_alpha()
        self.snake_head = self.snake_head_init
        self.prev_x = self.x = position[PROP_COORDINATES_X]
        self.prev_y = self.y = position[PROP_COORDINATES_Y]

    def draw(self):
        self.parent_screen.blit(self.snake_head, (self.x, self.y))

    def get_position(self):
        return (self.x, self.y), (self.prev_x, self.prev_y)

    def set_position(self, position):
        self.prev_x = self.x
        self.prev_y = self.y
        self.x = position[PROP_COORDINATES_X]
        self.y = position[PROP_COORDINATES_Y]

    def get_orientation(self):
        return self.orientation, self.prev_orientation

    def set_orientation(self, orientation):
        self.prev_orientation = self.orientation
        self.orientation = orientation

    def rotate_head(self, orientation = -1):
        if orientation != -1:
            self.set_orientation(orientation)
        self.snake_head = pygame.transform.rotate(self.snake_head_init, (PROP_ROTATION_STEP * self.orientation))