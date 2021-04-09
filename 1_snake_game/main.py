import pygame
from pygame.locals import *
import time
import random

BACKGROUND_COLOUR = (108, 165, 68) #(110, 110, 5)
SCREEN_SIZE = (1000, 800)
STARTING_SNAKE_SIZE = 5
STARTING_MOVEMENT_DELAY = 0.1
BLOCK_SIZE = 30
SCORE_BACKGROUND_COLOUR = (200,200,200)
SCORE_POSITION = (850,10)
SCORE_FONT_STYLE = 'arial'
SCORE_FONT_SIZE = 30
APPLE_IMAGE = "resources/appleSmall.jpg"
BLOCK_IMAGE = "resources/blockSmall.jpg"

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load(APPLE_IMAGE).convert()
        self.x = random.randint(1,int(SCREEN_SIZE[0]/BLOCK_SIZE))*BLOCK_SIZE
        self.y = random.randint(1,int(SCREEN_SIZE[1]/BLOCK_SIZE))*BLOCK_SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,int(SCREEN_SIZE[0]/BLOCK_SIZE))*BLOCK_SIZE
        self.y = random.randint(1,int(SCREEN_SIZE[1]/BLOCK_SIZE))*BLOCK_SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.image = pygame.image.load(BLOCK_IMAGE).convert()
        self.direction = 'down'

        self.length = length
        self.x = [BLOCK_SIZE]*length
        self.y = [BLOCK_SIZE]*length

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        if self.direction == 'left':
            self.x[0] -= BLOCK_SIZE
        if self.direction == 'right':
            self.x[0] += BLOCK_SIZE
        if self.direction == 'up':
            self.y[0] -= BLOCK_SIZE
        if self.direction == 'down':
            self.y[0] += BLOCK_SIZE

        self.draw()

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOUR)

        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode(SCREEN_SIZE)
        self.snake = Snake(self.surface, STARTING_SNAKE_SIZE)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + BLOCK_SIZE:
            if y1 >= y2 and y1 < y2 + BLOCK_SIZE:
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont(SCORE_FONT_STYLE, SCORE_FONT_SIZE)
        score = font.render(f"Score: {self.snake.length}",True,SCORE_BACKGROUND_COLOUR)
        self.surface.blit(score,SCORE_POSITION)

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_LEFT:
                        self.snake.move_left()

                    if event.key == K_RIGHT:
                        self.snake.move_right()

                    if event.key == K_UP:
                        self.snake.move_up()

                    if event.key == K_DOWN:
                        self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            self.play()

            time.sleep(STARTING_MOVEMENT_DELAY)

if __name__ == '__main__':
    game = Game()
    game.run()
