import pygame

DIR_RESOURCES = "resources/"
FILE_IMAGE_SPRITE_HEAD = DIR_RESOURCES + "snakeHeadSm.jpg"
FILE_IMAGE_SPRITE_BODY = DIR_RESOURCES + "snakeBodySm.jpg"
FILE_IMAGE_SPRITE_TAIL = DIR_RESOURCES + "snakeTailSm.jpg"

PROP_MOVE_DIRECTION_LEFT = 1
PROP_MOVE_DIRECTION_UP = 2
PROP_MOVE_DIRECTION_RIGHT = 3
PROP_MOVE_DIRECTION_DOWN = 4

PROP_SIZE_BLOCK = 30

class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.snake_head_init = pygame.image.load(FILE_IMAGE_SPRITE_HEAD).convert()
        self.snake_head = pygame.image.load(FILE_IMAGE_SPRITE_HEAD).convert()
        self.snake_body = pygame.image.load(FILE_IMAGE_SPRITE_BODY).convert()
        self.snake_tail_init = pygame.image.load(FILE_IMAGE_SPRITE_TAIL).convert()
        self.snake_tail = pygame.image.load(FILE_IMAGE_SPRITE_TAIL).convert()
        self.direction = PROP_MOVE_DIRECTION_DOWN
        self.length = length
        self.x = [PROP_SIZE_BLOCK] * length
        self.y = [PROP_SIZE_BLOCK] * length

    def move_left(self):
        self.direction = PROP_MOVE_DIRECTION_LEFT
        self.snake_head = pygame.transform.rotate(self.snake_head_init, 270)

    def move_right(self):
        self.direction = PROP_MOVE_DIRECTION_RIGHT
        self.snake_head = pygame.transform.rotate(self.snake_head_init, 90)

    def move_up(self):
        self.direction = PROP_MOVE_DIRECTION_UP
        self.snake_head = pygame.transform.rotate(self.snake_head_init, 180)

    def move_down(self):
        self.direction = PROP_MOVE_DIRECTION_DOWN
        self.snake_head = self.snake_head_init

    def walk(self):
        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        if self.direction == PROP_MOVE_DIRECTION_LEFT:
            self.x[0] -= PROP_SIZE_BLOCK
        if self.direction == PROP_MOVE_DIRECTION_RIGHT:
            self.x[0] += PROP_SIZE_BLOCK
        if self.direction == PROP_MOVE_DIRECTION_UP:
            self.y[0] -= PROP_SIZE_BLOCK
        if self.direction == PROP_MOVE_DIRECTION_DOWN:
            self.y[0] += PROP_SIZE_BLOCK

        self.draw()

    def draw(self):
        self.parent_screen.blit(self.snake_head, (self.x[0], self.y[0]))
        for i in range(1, self.length):
            self.parent_screen.blit(self.snake_body, (self.x[i], self.y[i]))

        if self.length > 2:
            self.parent_screen.blit(self.snake_tail, (self.x[self.length-1], self.y[self.length-1]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)