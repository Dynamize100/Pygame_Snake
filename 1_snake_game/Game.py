import pygame
from pygame.locals import KEYDOWN, QUIT, K_UP, K_LEFT, K_DOWN, K_RIGHT, K_RETURN, K_ESCAPE
from random import randint
from time import sleep
from Apple import Apple
from Snake import Snake
from Rock import Rock

COLOUR_BG_SCORE = (200, 200, 200)
COLOUR_FONT_SCORE = (00, 00, 00)

DIR_RESOURCES = "resources/"
FILE_IMAGE_SCORE_TEXT = DIR_RESOURCES + "scoreText.png"
FILE_IMAGE_SCORE_NUMBER = [
    DIR_RESOURCES + "scoreZero.png",
    DIR_RESOURCES + "scoreOne.png",
    DIR_RESOURCES + "scoreTwo.png",
    DIR_RESOURCES + "scoreThree.png",
    DIR_RESOURCES + "scoreFour.png",
    DIR_RESOURCES + "scoreFive.png",
    DIR_RESOURCES + "scoreSix.png",
    DIR_RESOURCES + "scoreSeven.png",
    DIR_RESOURCES + "scoreEight.png",
    DIR_RESOURCES + "scoreNine.png",
]

FILE_IMAGE_ARROW_UP = DIR_RESOURCES + "arrowUp.png"
FILE_IMAGE_ARROW_RIGHT = DIR_RESOURCES + "arrowRight.png"
FILE_IMAGE_ARROW_DOWN = DIR_RESOURCES + "arrowDown.png"
FILE_IMAGE_ARROW_LEFT = DIR_RESOURCES + "arrowLeft.png"
FILE_IMAGE_ARROW_NONE = DIR_RESOURCES + "arrowNone.png"

FILE_IMAGE_BK_GAME = DIR_RESOURCES + "Main_BK_1000x900.png"
FILE_IMAGE_BK_INTRO = DIR_RESOURCES + "Intro_BK_1000x900.png"
FILE_IMAGE_BK_END = DIR_RESOURCES + "End_BK_1000x900.png"

FILE_IMAGE_DETAILS_BK = DIR_RESOURCES + "Detail_Bk.png"

FILE_SOUND_EFFECT_CRASH = DIR_RESOURCES + "crash.mp3"
FILE_SOUND_EFFECT_BITE = DIR_RESOURCES + "appleBite.mp3"
FILE_SOUND_MUSIC_BG_MAIN = DIR_RESOURCES + "bg_music_1.mp3"

PROP_COORDINATES_X = 0
PROP_COORDINATES_Y = 1

PROP_FONT_STYLE_DETAILS = "georgia"
PROP_FONT_SIZE_SCORE = 20

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

PROP_POS_PLAY_ARROW_ONE = (350,10)
PROP_POS_PLAY_ARROW_TWO = (350,35)
PROP_POS_PLAY_ARROW_THREE = (350,60)

PROP_POS_END_ARROW_ONE = (550,210)
PROP_POS_END_ARROW_TWO = (550,235)
PROP_POS_END_ARROW_THREE = (550,260)

PROP_POS_END_DETAILS_BK = (245,210)
PROP_POS_END_STEP_COUNTER = (250, 212)

PROP_POS_PLAY_DETAILS_BK = (45,10)
PROP_POS_PLAY_STEP_COUNTER = (50, 12)

PROP_POSITION_SCORE = (850, 10)
PROP_POS_PLAY_SCORE_TEXT = (570, 2)
PROP_POS_PLAY_SCORE_MSB = (780, 10)
PROP_POS_PLAY_SCORE_MID = (840, 10)
PROP_POS_PLAY_SCORE_LSB = (900, 10)

PROP_POS_END_SCORE_TEXT = (290, 392)
PROP_POS_END_SCORE_MSB = (500, 400)
PROP_POS_END_SCORE_MID = (560, 400)
PROP_POS_END_SCORE_LSB = (620, 400)

PROP_RETRIEVE_ORIENT_CURRENT = 0
PROP_RETRIEVE_ORIENT_PREVIOUS = 1
PROP_RETRIEVE_POS_CURRENT = 0
PROP_RETRIEVE_POS_PREVIOUS = 1

PROP_SCREEN_INTRO = 0
PROP_SCREEN_PLAY = 1
PROP_SCREEN_END = 2

PROP_SIZE_BLOCK = 30
PROP_SIZE_SCREEN_WIDTH = 1000
PROP_SIZE_SCREEN_HEIGHT = 900
PROP_SIZE_SCREEN = (PROP_SIZE_SCREEN_WIDTH, PROP_SIZE_SCREEN_HEIGHT)
PROP_SIZE_SNAKE_INIT = 1
PROP_SIZE_FLOOR_MUL = 2
PROP_SIZE_TITLE_MUL = 4

PROP_SOUND_MUSIC_BG_LOOP = -1
PROP_SOUND_MUSIC_BG_START = 2
PROP_SOUND_MUSIC_BG_FADE = 2000

SOUND_EFFECT_CRASH = 0
SOUND_EFFECT_BITE = 1
SOUND_VOLUME_MAIN = 0.1

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Codebasics Snake And Apple Game")

        pygame.mixer.init()
        pygame.mixer.music.set_volume(SOUND_VOLUME_MAIN)
        self.play_background_music()
        self.step_counter = 0
        self.surface = pygame.display.set_mode(PROP_SIZE_SCREEN)
        self.snake = Snake(self.surface, PROP_SIZE_SNAKE_INIT)
        self.score_text = pygame.image.load(FILE_IMAGE_SCORE_TEXT).convert_alpha()
        self.score_msb = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[0]).convert_alpha()
        self.score_mid = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[0]).convert_alpha()
        self.score_lsb = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[0]).convert_alpha()
        self.details_bk = pygame.image.load(FILE_IMAGE_DETAILS_BK).convert_alpha()
        self.arrow_one = pygame.image.load(FILE_IMAGE_ARROW_NONE).convert_alpha()
        self.arrow_two = pygame.image.load(FILE_IMAGE_ARROW_NONE).convert_alpha()
        self.arrow_three = pygame.image.load(FILE_IMAGE_ARROW_NONE).convert_alpha()
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
        elif sound_name == SOUND_EFFECT_BITE:
            sound = pygame.mixer.Sound(FILE_SOUND_EFFECT_BITE)

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake.length = 1
        self.step_counter = 0
        self.snake = Snake(self.surface, PROP_SIZE_SNAKE_INIT)
        self.apple = Apple(self.surface)
        self.rock = Rock(self.surface)
        self.adjust_speed(PROP_MOVE_SPEED_RESET, None)
        self.score_mid = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[0]).convert_alpha()
        self.score_mid = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[0]).convert_alpha()
        self.score_lsb = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[0]).convert_alpha()

    def is_collision(self, snake, object):
        if snake[PROP_COORDINATES_X] >= object[PROP_COORDINATES_X] and snake[PROP_COORDINATES_X] < object[PROP_COORDINATES_X] + PROP_SIZE_BLOCK:
            if snake[PROP_COORDINATES_Y] >= object[PROP_COORDINATES_Y] and snake[PROP_COORDINATES_Y] < object[PROP_COORDINATES_Y] + PROP_SIZE_BLOCK:
                return True
        return False

    def is_boundary_collision(self, snake, screen_size):
        if snake[PROP_COORDINATES_X] < PROP_SIZE_BLOCK or snake[PROP_COORDINATES_X] + PROP_SIZE_BLOCK > screen_size[PROP_COORDINATES_X]-PROP_SIZE_BLOCK or \
                snake[PROP_COORDINATES_Y] < PROP_SIZE_BLOCK*PROP_SIZE_TITLE_MUL or snake[PROP_COORDINATES_Y] > screen_size[PROP_COORDINATES_Y]-PROP_SIZE_BLOCK*PROP_SIZE_FLOOR_MUL:
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
        self.step_counter += 1
        self.display_score("Play")
        self.apple.draw()
        self.rock.draw()
        self.snake.walk()

        # snake eating apple scenario
        if self.is_collision(self.snake.head.get_position()[PROP_RETRIEVE_POS_CURRENT], (self.apple.x, self.apple.y)):
            self.play_sound(SOUND_EFFECT_BITE)

            if self.snake.length > 99:
                self.score_mid = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[int((self.snake.length - self.snake.length % 100)/100)]).convert_alpha()
                self.score_mid = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[int((self.snake.length - self.snake.length % 10)/10)]).convert_alpha()
                self.score_lsb = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[self.snake.length % 10]).convert_alpha()
            elif self.snake.length > 9:
                self.score_mid = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[int((self.snake.length - self.snake.length % 10)/10)]).convert_alpha()
                self.score_lsb = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[self.snake.length % 10]).convert_alpha()
            else:
                self.score_lsb = pygame.image.load(FILE_IMAGE_SCORE_NUMBER[self.snake.length]).convert_alpha()

            # speed up the snake every x eating events
            if self.snake.length % PROP_MOVE_SPEED_UP_THRESHOLD == 0:
                self.adjust_speed(PROP_MOVE_SPEED_UP, PROP_MOVE_DELAY_INCREMENT)
                colours = ["Blank", "Black", "Blue", "Green", "Red", "White"]
                self.snake.set_colour(colours[randint(0, len(colours)-1)])

            self.snake.increase_length()
            # ToDo: Check if the apple has landed on the snake or rock
            self.apple.move()
            if self.is_collision(self.apple.get_position(), self.rock.get_position()):
                self.apple.move()
            # ToDo: Move the rock every so often.

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

        self.surface.blit(self.arrow_one, PROP_POS_PLAY_ARROW_ONE)
        self.surface.blit(self.arrow_two, PROP_POS_PLAY_ARROW_TWO)
        self.surface.blit(self.arrow_three, PROP_POS_PLAY_ARROW_THREE)

        pygame.display.flip()

    def display_score(self, screen):
        if screen == "Play":
            distance_font = pygame.font.SysFont(PROP_FONT_STYLE_DETAILS, PROP_FONT_SIZE_SCORE)
            step_counter = distance_font.render(f"Distance: {self.step_counter/4}m", True, COLOUR_FONT_SCORE)

            det = PROP_POS_PLAY_DETAILS_BK
            dist = PROP_POS_PLAY_STEP_COUNTER
            text = PROP_POS_PLAY_SCORE_TEXT
            msb = PROP_POS_PLAY_SCORE_MSB
            mid = PROP_POS_PLAY_SCORE_MID
            lsb = PROP_POS_PLAY_SCORE_LSB
        elif screen == "End":
            distance_font = pygame.font.SysFont(PROP_FONT_STYLE_DETAILS, PROP_FONT_SIZE_SCORE)
            step_counter = distance_font.render(f"Distance: {self.step_counter/4}m", True, COLOUR_FONT_SCORE)

            det = PROP_POS_END_DETAILS_BK
            dist = PROP_POS_END_STEP_COUNTER
            text = PROP_POS_END_SCORE_TEXT
            msb = PROP_POS_END_SCORE_MSB
            mid = PROP_POS_END_SCORE_MID
            lsb = PROP_POS_END_SCORE_LSB
        else:
            distance_font = pygame.font.SysFont(PROP_FONT_STYLE_DETAILS, PROP_FONT_SIZE_SCORE)
            step_counter = distance_font.render(f"Distance: {self.step_counter/4}m", True, COLOUR_FONT_SCORE)

            det = PROP_POS_PLAY_DETAILS_BK
            dist = PROP_POS_PLAY_STEP_COUNTER
            text = PROP_POS_END_SCORE_TEXT
            msb = PROP_POS_END_SCORE_MSB
            mid = PROP_POS_END_SCORE_MID
            lsb = PROP_POS_END_SCORE_LSB

        self.surface.blit(self.details_bk, det)
        self.surface.blit(step_counter, dist)
        self.surface.blit(self.score_text, text)
        self.surface.blit(self.score_msb, msb)
        self.surface.blit(self.score_mid, mid)
        self.surface.blit(self.score_lsb, lsb)

    def show_intro(self):
        self.render_background(FILE_IMAGE_BK_INTRO)
        self.play_background_music()
        pygame.mixer.music.pause()
        pygame.display.flip()

    def show_game_over(self):
        self.render_background(FILE_IMAGE_BK_END)
        self.display_score("End")

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
                        self.arrow_one = self.arrow_two
                        self.arrow_two = self.arrow_three
                        self.arrow_three = pygame.image.load(FILE_IMAGE_ARROW_LEFT).convert_alpha()

                    elif event.key == K_RIGHT:
                        self.snake.turn(PROP_MOVE_DIRECTION_RIGHT)
                        self.arrow_one = self.arrow_two
                        self.arrow_two = self.arrow_three
                        self.arrow_three = pygame.image.load(FILE_IMAGE_ARROW_RIGHT).convert_alpha()

                    elif event.key == K_UP:
                        self.snake.turn(PROP_MOVE_DIRECTION_UP)
                        self.arrow_one = self.arrow_two
                        self.arrow_two = self.arrow_three
                        self.arrow_three = pygame.image.load(FILE_IMAGE_ARROW_UP).convert_alpha()

                    elif event.key == K_DOWN:
                        self.snake.turn(PROP_MOVE_DIRECTION_DOWN)
                        self.arrow_one = self.arrow_two
                        self.arrow_two = self.arrow_three
                        self.arrow_three = pygame.image.load(FILE_IMAGE_ARROW_DOWN).convert_alpha()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()

            except Exception as e:
                pause = True
                self.show_game_over()
                self.reset()

            sleep(self.move_delay)

    def run_end(self):
        running = True
        self.show_game_over()
        self.reset()
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
