import pygame

DIR_RESOURCES = "resources/"
FILE_IMAGE_BODY_BLANK = DIR_RESOURCES + "snakeBodySmBlank.png"
FILE_IMAGE_BODY_BLACK = DIR_RESOURCES + "snakeBodySmBlack.png"
FILE_IMAGE_BODY_BLUE = DIR_RESOURCES + "snakeBodySmBlue.png"
FILE_IMAGE_BODY_GREEN = DIR_RESOURCES + "snakeBodySmGreen.png"
FILE_IMAGE_BODY_RED = DIR_RESOURCES + "snakeBodySmRed.png"
FILE_IMAGE_BODY_WHITE = DIR_RESOURCES + "snakeBodySmWhite.png"

PROP_SIZE_BLOCK = 30
PROP_SIZE_SCREEN_WIDTH = 1000
PROP_SIZE_SCREEN_HEIGHT = 800

PROP_COORDINATES_X = 0
PROP_COORDINATES_Y = 1

PROP_ORIENTATION_SOUTH = 0

PROP_ROTATION_STEP = 90

class SnakeBodyBlock:
    def __init__(self, parent_screen, position):
        self.parent_screen = parent_screen
        self.orientation = PROP_ORIENTATION_SOUTH
        self.colour = "Red"
        self.prev_orientation = self.orientation
        self.snake_body_init = pygame.image.load(FILE_IMAGE_BODY_RED).convert_alpha()
        self.snake_body = self.snake_body_init
        self.prev_x = self.x = position[PROP_COORDINATES_X]
        self.prev_y = self.y = position[PROP_COORDINATES_Y]

    def draw(self):
        self.parent_screen.blit(self.snake_body, (self.x, self.y))

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

    def get_colour(self):
        return self.colour

    def set_colour(self, colour):
        self.colour = colour
        if colour == "Black":
            self.snake_body = pygame.image.load(FILE_IMAGE_BODY_BLACK).convert_alpha()
        elif colour == "Blue":
            self.snake_body = pygame.image.load(FILE_IMAGE_BODY_BLUE).convert_alpha()
        elif colour == "Green":
            self.snake_body = pygame.image.load(FILE_IMAGE_BODY_GREEN).convert_alpha()
        elif colour == "Red":
            self.snake_body = pygame.image.load(FILE_IMAGE_BODY_RED).convert_alpha()
        elif colour == "White":
            self.snake_body = pygame.image.load(FILE_IMAGE_BODY_WHITE).convert_alpha()
        else:
            self.snake_body = pygame.image.load(FILE_IMAGE_BODY_BLANK).convert_alpha()

    def rotate_body_block(self, orientation=-1):
        if orientation != -1:
            self.set_orientation(orientation)
        self.snake_body = pygame.transform.rotate(self.snake_body_init, (PROP_ROTATION_STEP * self.orientation))