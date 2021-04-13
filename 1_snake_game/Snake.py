import pygame

from SnakeHead import SnakeHead as head
from SnakeBodyBlock import SnakeBodyBlock as body_block
from SnakeTail import SnakeTail as tail
from random import randint

DIR_RESOURCES = "resources/"
FILE_IMAGE_SPRITE_HEAD = DIR_RESOURCES + "snakeHeadSm.jpg"
FILE_IMAGE_SPRITE_BODY = DIR_RESOURCES + "snakeBodySm.jpg"
FILE_IMAGE_SPRITE_TAIL = DIR_RESOURCES + "snakeTailSm.jpg"

PROP_MOVE_DIRECTION_DOWN = 0
PROP_MOVE_DIRECTION_RIGHT = 1
PROP_MOVE_DIRECTION_UP = 2
PROP_MOVE_DIRECTION_LEFT = 3

PROP_COORDINATES_X = 0
PROP_COORDINATES_Y = 1

PROP_RETRIEVE_ORIENT_CURRENT = 0
PROP_RETRIEVE_ORIENT_PREVIOUS = 1
PROP_RETRIEVE_POS_CURRENT = 0
PROP_RETRIEVE_POS_PREVIOUS = 1

PROP_SIZE_BLOCK = 30
PROP_SIZE_SCREEN_WIDTH = 1000
PROP_SIZE_SCREEN_HEIGHT = 900

class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.length = length
        self.direction = PROP_MOVE_DIRECTION_RIGHT
        #self.position = (
        #    randint(3, int(PROP_SIZE_SCREEN_WIDTH / PROP_SIZE_BLOCK) - 3) * PROP_SIZE_BLOCK,
        #    randint(3, int(PROP_SIZE_SCREEN_HEIGHT / PROP_SIZE_BLOCK) - 3) * PROP_SIZE_BLOCK
        #)
        self.position = (0, (PROP_SIZE_SCREEN_HEIGHT+PROP_SIZE_BLOCK)/2)
        self.head = head(self.parent_screen, self.position)
        self.body = [body_block(self.parent_screen, self.position)] * (self.length)
        self.tail = tail(self.parent_screen, self.position)

    def turn(self, direction):
        self.direction = direction

    def walk(self):
        if self.direction == PROP_MOVE_DIRECTION_LEFT:
            self.position = (self.position[PROP_COORDINATES_X] - PROP_SIZE_BLOCK, self.position[PROP_COORDINATES_Y])
        if self.direction == PROP_MOVE_DIRECTION_RIGHT:
            self.position = (self.position[PROP_COORDINATES_X] + PROP_SIZE_BLOCK, self.position[PROP_COORDINATES_Y])
        if self.direction == PROP_MOVE_DIRECTION_UP:
            self.position = (self.position[PROP_COORDINATES_X], self.position[PROP_COORDINATES_Y] - PROP_SIZE_BLOCK)
        if self.direction == PROP_MOVE_DIRECTION_DOWN:
            self.position = (self.position[PROP_COORDINATES_X], self.position[PROP_COORDINATES_Y] + PROP_SIZE_BLOCK)

        self.head.set_position(self.position)
        self.head.set_orientation(self.direction)
        self.head.rotate_head()

        self.body[len(self.body) - 1].set_position(self.head.get_position()[PROP_RETRIEVE_POS_PREVIOUS])
        self.body[len(self.body) - 1].set_orientation(self.head.get_orientation()[PROP_RETRIEVE_ORIENT_PREVIOUS])
        self.body[len(self.body) - 1].rotate_body_block()

        for i in range(len(self.body) - 2, -1, -1):
            self.body[i].set_position(self.body[i + 1].get_position()[PROP_RETRIEVE_POS_PREVIOUS])
            self.body[i].set_orientation(self.body[i + 1].get_orientation()[PROP_RETRIEVE_ORIENT_PREVIOUS])
            self.body[i].rotate_body_block()

        self.tail.set_position(self.body[0].get_position()[PROP_RETRIEVE_POS_PREVIOUS])
        self.tail.set_orientation(self.body[0].get_orientation()[PROP_RETRIEVE_ORIENT_PREVIOUS])
        self.tail.rotate_tail()

        self.draw()

    def draw(self):
        self.head.draw()
        for i in range(len(self.body) - 1, -1, -1):
            self.body[i].draw()
        self.tail.draw()

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.body.insert(0, body_block(self.parent_screen, self.position))