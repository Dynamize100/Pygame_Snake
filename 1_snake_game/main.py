import pygame
from pygame.locals import KEYDOWN, QUIT, K_UP, K_LEFT, K_DOWN, K_RIGHT, K_RETURN, K_ESCAPE
from random import randint
from time import sleep

COLOUR_BG = (108, 165, 68) #(110, 110, 5)
COLOUR_BG_GAME_OVER = (108, 165, 68) #(110, 110, 5)
COLOUR_BG_SCORE = (200, 200, 200)
COLOUR_FONT_SCORE = (68, 165, 108)

DIR_RESOURCES = "resources/"
FILE_IMAGE_SPRITE_APPLE = DIR_RESOURCES + "appleSmall.jpg"
FILE_IMAGE_SPRITE_BLOCK = DIR_RESOURCES + "blockSmall.jpg"

PROP_SIZE_BLOCK = 30
PROP_SIZE_SCREEN = (1000, 800)
PROP_SIZE_SNAKE_INIT = 1
PROP_POSITION_SCORE = (850, 10)
PROP_MOVE_DELAY_INIT = 0.1

PROP_MOVE_DIRECTION_LEFT = 1
PROP_MOVE_DIRECTION_UP = 2
PROP_MOVE_DIRECTION_RIGHT = 3
PROP_MOVE_DIRECTION_DOWN = 4

PROP_FONT_STYLE_SCORE = 'arial'
PROP_FONT_SIZE_SCORE = 30

SOUND_EFFECT_CRASH = 0
SOUND_EFFECT_DING = 1

FILE_SOUND_EFFECT_CRASH = DIR_RESOURCES + "crash.mp3"
FILE_SOUND_EFFECT_DING = DIR_RESOURCES + "ding.mp3"
FILE_SOUND_MUSIC_BG_MAIN = DIR_RESOURCES + "bg_music_1.mp3"

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load(FILE_IMAGE_SPRITE_APPLE).convert()
        self.x = randint(1, int(PROP_SIZE_SCREEN[0] / PROP_SIZE_BLOCK) - 1) * PROP_SIZE_BLOCK
        self.y = randint(1, int(PROP_SIZE_SCREEN[1] / PROP_SIZE_BLOCK) - 1) * PROP_SIZE_BLOCK

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = randint(1, int(PROP_SIZE_SCREEN[0] / PROP_SIZE_BLOCK) - 1) * PROP_SIZE_BLOCK
        self.y = randint(1, int(PROP_SIZE_SCREEN[1] / PROP_SIZE_BLOCK) - 1) * PROP_SIZE_BLOCK


class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.image = pygame.image.load(FILE_IMAGE_SPRITE_BLOCK).convert()
        self.direction = PROP_MOVE_DIRECTION_DOWN

        self.length = length
        self.x = [PROP_SIZE_BLOCK] * length
        self.y = [PROP_SIZE_BLOCK] * length

    def move_left(self):
        self.direction = PROP_MOVE_DIRECTION_LEFT

    def move_right(self):
        self.direction = PROP_MOVE_DIRECTION_RIGHT

    def move_up(self):
        self.direction = PROP_MOVE_DIRECTION_UP

    def move_down(self):
        self.direction = PROP_MOVE_DIRECTION_DOWN

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
        self.parent_screen.fill(COLOUR_BG)

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
        pygame.display.set_caption("Codebasics Snake And Apple Game")
        self.surface = pygame.display.set_mode(PROP_SIZE_SCREEN)
        self.snake = Snake(self.surface, PROP_SIZE_SNAKE_INIT)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play_background_music(self):
        pygame.mixer.music.load(FILE_SOUND_MUSIC_BG_MAIN)
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == SOUND_EFFECT_CRASH:
            sound = pygame.mixer.Sound(FILE_SOUND_EFFECT_CRASH)
        elif sound_name == SOUND_EFFECT_DING:
            sound = pygame.mixer.Sound(FILE_SOUND_EFFECT_DING)

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface, PROP_SIZE_SNAKE_INIT)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + PROP_SIZE_BLOCK:
            if y1 >= y2 and y1 < y2 + PROP_SIZE_BLOCK:
                return True
        return False

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple scenario
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound(SOUND_EFFECT_DING)
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound(SOUND_EFFECT_CRASH)
                raise Exception("Collision Occurred")

    def display_score(self):
        font = pygame.font.SysFont(PROP_FONT_STYLE_SCORE, PROP_FONT_SIZE_SCORE)
        score = font.render(f"Score: {self.snake.length}",True,COLOUR_BG_SCORE)
        self.surface.blit(score,PROP_POSITION_SCORE)

    def show_game_over(self):
        self.surface.fill(COLOUR_BG_GAME_OVER)
        font = pygame.font.SysFont(PROP_FONT_STYLE_SCORE, PROP_FONT_SIZE_SCORE)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, COLOUR_FONT_SCORE)
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, COLOUR_FONT_SCORE)
        self.surface.blit(line2, (200, 350))

        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False

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

            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            sleep(PROP_MOVE_DELAY_INIT)

if __name__ == '__main__':
    game = Game()
    game.run()
