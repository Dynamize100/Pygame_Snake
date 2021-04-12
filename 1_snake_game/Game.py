import pygame
from pygame.locals import KEYDOWN, QUIT, K_UP, K_LEFT, K_DOWN, K_RIGHT, K_RETURN, K_ESCAPE
from time import sleep
from Apple import Apple
from Snake import Snake
from Rock import Rock

COLOUR_BG_SCORE = (200, 200, 200)
COLOUR_FONT_SCORE = (255, 00, 00)

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
FILE_IMAGE_BK_INTRO = DIR_RESOURCES + "Intro_BK.png"
FILE_IMAGE_BK_END = DIR_RESOURCES + "End_BK.png"

FILE_SOUND_EFFECT_CRASH = DIR_RESOURCES + "crash.mp3"
FILE_SOUND_EFFECT_DING = DIR_RESOURCES + "appleBite.mp3"
FILE_SOUND_MUSIC_BG_MAIN = DIR_RESOURCES + "bg_music_1.mp3"

PROP_COORDINATES_X = 0
PROP_COORDINATES_Y = 1

PROP_FONT_STYLE_SCORE = "arial"
PROP_FONT_SIZE_SCORE = 50

PROP_MOVE_DELAY_MAX = 1
PROP_MOVE_DELAY_MIN = 0.025
PROP_MOVE_DELAY_INCREMENT = 0.025
PROP_MOVE_DELAY_INIT = PROP_MOVE_DELAY_MAX / 8

PROP_MOVE_DIRECTION_DOWN = 0
PROP_MOVE_DIRECTION_RIGHT = 1
PROP_MOVE_DIRECTION_UP = 2
PROP_MOVE_DIRECTION_LEFT = 3

PROP_MOVE_SPEED_DOWN = 0
PROP_MOVE_SPEED_RESET = -1
PROP_MOVE_SPEED_UP = 1
PROP_MOVE_SPEED_UP_THRESHOLD = 3

PROP_POSITION_SCORE = (850, 10)
PROP_POSITION_SCORE_TEXT = (620, 10)
PROP_POSITION_SCORE_MSB = (820, 10)
PROP_POSITION_SCORE_MID = (880, 10)
PROP_POSITION_SCORE_LSB = (940, 10)

PROP_RETRIEVE_ORIENT_CURRENT = 0
PROP_RETRIEVE_ORIENT_PREVIOUS = 1
PROP_RETRIEVE_POS_CURRENT = 0
PROP_RETRIEVE_POS_PREVIOUS = 1

PROP_SCREEN_INTRO = 0
PROP_SCREEN_PLAY = 1
PROP_SCREEN_END = 2

PROP_SIZE_BLOCK = 30
PROP_SIZE_SCREEN_WIDTH = 1000
PROP_SIZE_SCREEN_HEIGHT = 800
PROP_SIZE_SCREEN = (PROP_SIZE_SCREEN_WIDTH, PROP_SIZE_SCREEN_HEIGHT)
PROP_SIZE_SNAKE_INIT = 1

PROP_SOUND_MUSIC_BG_LOOP = -1
PROP_SOUND_MUSIC_BG_START = 2
PROP_SOUND_MUSIC_BG_FADE = 2000

SOUND_EFFECT_CRASH = 0
SOUND_EFFECT_DING = 1
SOUND_VOLUME_MAIN = 0.1

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Codebasics Snake And Apple Game")

        pygame.mixer.init()
        pygame.mixer.music.set_volume(SOUND_VOLUME_MAIN)
        self.play_background_music()

        self.surface = pygame.display.set_mode(PROP_SIZE_SCREEN)
        self.snake = Snake(self.surface, PROP_SIZE_SNAKE_INIT)
        self.score_text = pygame.image.load(FILE_IMAGE_SCORE_TEXT).convert()
        self.score_msb = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[0]).convert()
        self.score_mid = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[0]).convert()
        self.score_lsb = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[0]).convert()
        self.move_delay = PROP_MOVE_DELAY_INIT
        self.screen_current = PROP_SCREEN_INTRO # ToDo: This need to be set back to intro
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.rock = Rock(self.surface)
        self.rock.draw()

    def play_background_music(self):
        pygame.mixer.music.load(FILE_SOUND_MUSIC_BG_MAIN)
        pygame.mixer.music.play(PROP_SOUND_MUSIC_BG_LOOP, PROP_SOUND_MUSIC_BG_START, PROP_SOUND_MUSIC_BG_FADE)

    def play_sound(self, sound_name):
        if sound_name == SOUND_EFFECT_CRASH:
            sound = pygame.mixer.Sound(FILE_SOUND_EFFECT_CRASH)
        elif sound_name == SOUND_EFFECT_DING:
            sound = pygame.mixer.Sound(FILE_SOUND_EFFECT_DING)

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface, PROP_SIZE_SNAKE_INIT)
        self.apple = Apple(self.surface)
        self.rock = Rock(self.surface)
        self.adjust_speed(PROP_MOVE_SPEED_RESET, None)

    def is_collision(self, snake, object):
        if snake[PROP_COORDINATES_X] >= object[PROP_COORDINATES_X] and snake[PROP_COORDINATES_X] < object[PROP_COORDINATES_X] + PROP_SIZE_BLOCK:
            if snake[PROP_COORDINATES_Y] >= object[PROP_COORDINATES_Y] and snake[PROP_COORDINATES_Y] < object[PROP_COORDINATES_Y] + PROP_SIZE_BLOCK:
                return True
        return False

    def is_boundary_collision(self, snake, screen_size):
        if snake[PROP_COORDINATES_X] < 0 or snake[PROP_COORDINATES_X] + PROP_SIZE_BLOCK > screen_size[PROP_COORDINATES_X] or \
                snake[PROP_COORDINATES_Y] < 0 or snake[PROP_COORDINATES_Y] > screen_size[PROP_COORDINATES_Y]:
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
            self.move_delay = PROP_MOVE_DELAY_MAX / 8

    def render_background(self, image):
        bg = pygame.image.load(image)
        self.surface.blit(bg, (0,0))

    def play(self):
        self.render_background(FILE_IMAGE_BK_GAME)
        self.display_score()
        self.apple.draw()
        self.rock.draw()
        self.snake.walk()

        pygame.display.flip()

        # snake eating apple scenario
        if self.is_collision(self.snake.head.get_position()[PROP_RETRIEVE_POS_CURRENT], (self.apple.x, self.apple.y)):
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

        # snake colliding with rock
        if self.is_collision(self.snake.head.get_position()[PROP_RETRIEVE_POS_CURRENT], (self.rock.x, self.rock.y)):
            self.play_sound(SOUND_EFFECT_CRASH)
            raise Exception("Snake collided with the rock")

        # snake colliding with body
        for i in range(len(self.snake.body) - 1, 0, -1):
            if self.is_collision(self.snake.head.get_position()[PROP_RETRIEVE_POS_CURRENT], self.snake.body[i].get_position()[PROP_RETRIEVE_POS_CURRENT]):
                self.play_sound(SOUND_EFFECT_CRASH)
                raise Exception("Snake collided with itself")

        # snake colliding with tail
        if self.is_collision(self.snake.head.get_position()[PROP_RETRIEVE_POS_CURRENT], self.snake.tail.get_position()[PROP_RETRIEVE_POS_CURRENT]):
            self.play_sound(SOUND_EFFECT_CRASH)
            raise Exception("Snake collided with the rock")

        # snake colliding with the boundary
        if self.is_boundary_collision(self.snake.head.get_position()[PROP_RETRIEVE_POS_CURRENT], PROP_SIZE_SCREEN):
            self.play_sound(SOUND_EFFECT_CRASH)
            raise Exception("Snake collided with the boundary")

    def display_score(self):
        self.surface.blit(self.score_text, PROP_POSITION_SCORE_TEXT)
        self.surface.blit(self.score_msb, PROP_POSITION_SCORE_MSB)
        self.surface.blit(self.score_mid, PROP_POSITION_SCORE_MID)
        self.surface.blit(self.score_lsb, PROP_POSITION_SCORE_LSB)

    def show_intro(self):
        self.render_background(FILE_IMAGE_BK_INTRO)
        self.play_background_music()
        pygame.mixer.music.pause()
        pygame.display.flip()


    def show_game_over(self):
        self.render_background(FILE_IMAGE_BK_END)
        font = pygame.font.SysFont(PROP_FONT_STYLE_SCORE, PROP_FONT_SIZE_SCORE)
        line1 = font.render(f"Score: {self.snake.length-1}", True, COLOUR_FONT_SCORE)
        self.surface.blit(line1, (700, 570))

        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        if self.screen_current == PROP_SCREEN_INTRO:
            self.run_intro()
        elif self.screen_current == PROP_SCREEN_PLAY:
            self.run_game()
        elif self.screen_current == PROP_SCREEN_END:
            self.run_end()
        else:
            pass

    def run_intro(self):
        running = True
        self.reset()
        self.show_intro()
        pygame.mixer.music.unpause()

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                        self.screen_current = PROP_SCREEN_INTRO

                    elif event.key == K_RETURN:
                        running = False
                        self.screen_current = PROP_SCREEN_PLAY
                        self.run()

    def run_game(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    elif event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()

                    elif event.key == K_LEFT:
                        self.snake.turn(PROP_MOVE_DIRECTION_LEFT)

                    elif event.key == K_RIGHT:
                        self.snake.turn(PROP_MOVE_DIRECTION_RIGHT)

                    elif event.key == K_UP:
                        self.snake.turn(PROP_MOVE_DIRECTION_UP)

                    elif event.key == K_DOWN:
                        self.snake.turn(PROP_MOVE_DIRECTION_DOWN)

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

    def run_end(self):
        running = True
        self.reset()
        self.show_game_over()
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                        self.screen_current = PROP_SCREEN_INTRO

                    elif event.key == K_RETURN:
                        running = False
                        self.screen_current = PROP_SCREEN_PLAY
                        self.run()





