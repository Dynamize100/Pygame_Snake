import pygame
from pygame.locals import KEYDOWN, QUIT, K_UP, K_LEFT, K_DOWN, K_RIGHT, K_RETURN, K_ESCAPE
from time import sleep
from Apple import Apple
from Snake import Snake

COLOUR_BG_SCORE = (200, 200, 200)
COLOUR_FONT_SCORE = (68, 165, 108)

DIR_RESOURCES = "resources/"
FILE_IMAGE_SCORE_TEXT = DIR_RESOURCES + "scoreText.jpg"
FILE_IMAGE_SCORE_NUMBER = [
    DIR_RESOURCES + "scoreZero.jpg",
    DIR_RESOURCES + "scoreOne.jpg",
    DIR_RESOURCES + "scoreTwo.jpg",
    DIR_RESOURCES + "scoreThree.jpg",
    DIR_RESOURCES + "scoreFour.jpg",
    DIR_RESOURCES + "scoreFive.jpg",
    DIR_RESOURCES + "scoreSix.jpg",
    DIR_RESOURCES + "scoreSeven.jpg",
    DIR_RESOURCES + "scoreEight.jpg",
    DIR_RESOURCES + "scoreNine.jpg",
]
FILE_IMAGE_BK_GAME = DIR_RESOURCES + "bgRealGrass_1000x800.jpg"
FILE_IMAGE_BK_END = DIR_RESOURCES + "background.jpg"

FILE_SOUND_EFFECT_CRASH = DIR_RESOURCES + "crash.mp3"
FILE_SOUND_EFFECT_DING = DIR_RESOURCES + "ding.mp3"
FILE_SOUND_MUSIC_BG_MAIN = DIR_RESOURCES + "bg_music_1.mp3"

PROP_FONT_STYLE_SCORE = "arial"
PROP_FONT_SIZE_SCORE = 30

PROP_MOVE_DELAY_MAX = 1
PROP_MOVE_DELAY_MIN = 0.025
PROP_MOVE_DELAY_INCREMENT = 0.025
PROP_MOVE_DELAY_INIT = PROP_MOVE_DELAY_MAX / 8

PROP_MOVE_SPEED_DOWN = 0
PROP_MOVE_SPEED_RESET = -1
PROP_MOVE_SPEED_UP = 1
PROP_MOVE_SPEED_UP_THRESHOLD = 3

PROP_POSITION_SCORE = (850, 10)
PROP_POSITION_SCORE_TEXT = (620, 10)
PROP_POSITION_SCORE_MSB = (820, 10)
PROP_POSITION_SCORE_MID = (880, 10)
PROP_POSITION_SCORE_LSB = (940, 10)

PROP_SIZE_BLOCK = 30
PROP_SIZE_SCREEN_WIDTH = 1000
PROP_SIZE_SCREEN_HEIGHT = 800
PROP_SIZE_SCREEN = (PROP_SIZE_SCREEN_WIDTH, PROP_SIZE_SCREEN_HEIGHT)
PROP_SIZE_SNAKE_INIT = 1

SOUND_EFFECT_CRASH = 0
SOUND_EFFECT_DING = 1

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Codebasics Snake And Apple Game")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode(PROP_SIZE_SCREEN)
        self.snake = Snake(self.surface, PROP_SIZE_SNAKE_INIT)
        self.score_text = pygame.image.load(FILE_IMAGE_SCORE_TEXT).convert()
        self.score_msb = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[0]).convert()
        self.score_mid = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[0]).convert()
        self.score_lsb = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[0]).convert()
        self.move_delay = PROP_MOVE_DELAY_INIT
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
        self.adjust_speed(PROP_MOVE_SPEED_RESET, None)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + PROP_SIZE_BLOCK:
            if y1 >= y2 and y1 < y2 + PROP_SIZE_BLOCK:
                return True
        return False

    def is_boundary_collision(self, x1, y1, width, height):
        if x1 < 0 or x1 + PROP_SIZE_BLOCK > width or y1 < 0 or y1 > height:
            return True
        return False

    def adjust_speed(self, direction, amount):
        if direction == PROP_MOVE_SPEED_DOWN:
            if self.move_delay + amount > PROP_MOVE_DELAY_MAX:
                self.move_delay = PROP_MOVE_DELAY_MAX
            else:
                self.move_delay += amount
        elif direction == PROP_MOVE_SPEED_UP:
            if self.move_delay - amount < PROP_MOVE_DELAY_MIN:
                self.move_delay = PROP_MOVE_DELAY_MIN
            else:
                self.move_delay -= amount
        else:
            self.move_delay = PROP_MOVE_DELAY_MAX / 2

    def render_background(self, image):
        bg = pygame.image.load(image)
        self.surface.blit(bg, (0,0))

    def play(self):
        self.render_background(FILE_IMAGE_BK_GAME)
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple scenario
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound(SOUND_EFFECT_DING)

            if self.snake.length > 99:
                self.score_mid = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[int((self.snake.length - self.snake.length % 100)/100)]).convert()
                self.score_mid = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[int((self.snake.length - self.snake.length % 10)/10)]).convert()
                self.score_lsb = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[self.snake.length % 10]).convert()
            elif self.snake.length > 9:
                self.score_mid = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[int((self.snake.length - self.snake.length % 10)/10)]).convert()
                self.score_lsb = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[self.snake.length % 10]).convert()
            else:
                self.score_lsb = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[self.snake.length]).convert()

            # speed up the snake every x eating events
            if self.snake.length % PROP_MOVE_SPEED_UP_THRESHOLD == 0:
                self.adjust_speed(PROP_MOVE_SPEED_UP, PROP_MOVE_DELAY_INCREMENT)

            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound(SOUND_EFFECT_CRASH)
                raise Exception("Snake collided with itself")

        # snake colliding with the boundary
        if self.is_boundary_collision(self.snake.x[0], self.snake.y[0], PROP_SIZE_SCREEN_WIDTH, PROP_SIZE_SCREEN_HEIGHT):
            self.play_sound(SOUND_EFFECT_CRASH)
            raise Exception("Snake collided with the boundary")

    def display_score(self):
        self.surface.blit(self.score_text, PROP_POSITION_SCORE_TEXT)
        self.surface.blit(self.score_msb, PROP_POSITION_SCORE_MSB)
        self.surface.blit(self.score_mid, PROP_POSITION_SCORE_MID)
        self.surface.blit(self.score_lsb, PROP_POSITION_SCORE_LSB)

    def show_game_over(self):
        self.render_background(FILE_IMAGE_BK_END)
        font = pygame.font.SysFont(PROP_FONT_STYLE_SCORE, PROP_FONT_SIZE_SCORE)
        line1 = font.render(f"Game is over! Your score is {self.snake.length-1}", True, COLOUR_FONT_SCORE)
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, COLOUR_FONT_SCORE)
        self.surface.blit(line2, (200, 350))

        pygame.mixer.music.pause()
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
                        pygame.mixer.music.unpause()

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

            sleep(self.move_delay)