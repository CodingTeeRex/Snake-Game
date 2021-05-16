from pygame.constants import KEYDOWN, K_ESCAPE, K_RETURN, K_r, QUIT, SWSURFACE
import pygame
from random import randint
from enum import Enum
from collections import namedtuple

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

pygame.init()
font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

point = namedtuple('point', 'x, y')

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREEN2 = (111, 255, 255)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 255, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 10

class snake_game:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Snake')

        self.direction = Direction.RIGHT
        self.head = point(self.width//2, self.height//2)
        self.body = [self.head, point(self.head.x - BLOCK_SIZE, self.head.y), point(self.head.x - 2*BLOCK_SIZE, self.head.y)]

        self.score = 0
        self.food = None
        self.spawn_food()
    
    def update_screen(self):
        # draw background
        self.screen.fill(BLACK)
        self.clock.tick(SPEED)

        # draw snake
        offset = 4
        for body_part in self.body:
            pygame.draw.rect(self.screen, BLUE1, pygame.Rect(body_part.x, body_part.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.screen, BLUE2, pygame.Rect(body_part.x + offset, body_part.y + offset, BLOCK_SIZE - offset*2, BLOCK_SIZE - offset*2))
        
        # draw food
        pygame.draw.rect(self.screen, GREEN, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.screen, GREEN2, pygame.Rect(self.food.x + offset, self.food.y + offset, BLOCK_SIZE - offset*2, BLOCK_SIZE - offset*2))

        # draw score board
        text = font.render(f"Score: {str(self.score)}", True, WHITE)
        self.screen.blit(text, [0, 0])
        pygame.display.update()

    def move(self, direction):
        x = self.head.x
        y = self.head.y

        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        if direction == Direction.LEFT:
            x -= BLOCK_SIZE
        if direction == Direction.DOWN:
            y += BLOCK_SIZE
        if direction == Direction.UP:
            y -= BLOCK_SIZE
        
        self.head = point(x, y)

    def spawn_food(self):
        x = randint(0, (self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = randint(0, (self.height-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = point(x, y)
        if self.food in self.body:
            self.spawn_food()
    
    def isCollision(self):
        if self.head.x < 0 or self.head.x > self.width - BLOCK_SIZE or self.head.y < 0 or self.head.y > self.height - BLOCK_SIZE:
            return True
        if self.head in self.body[1:]:
            return True
        
        return False

    def end_game_screen(self):
        self.screen.fill(BLACK)

        game_over_txt = font.render('GAME OVER', True, WHITE)
        game_over_txt_rect = game_over_txt.get_rect(center=(self.width/2, self.height/2))

        score_txt = font.render(f'Score: {str(self.score)}', True, WHITE)
        score_txt_rect = score_txt.get_rect(center=(self.width/2, self.height/2))

        continue_txt = font.render('Press ENTER key to play again!', True, WHITE)
        continue_txt_rect = continue_txt.get_rect(center=(self.width/2, self.height/2))

        self.screen.blit(game_over_txt, game_over_txt_rect)
        self.screen.blit(score_txt, [score_txt_rect[0], score_txt_rect[1]+25])
        self.screen.blit(continue_txt, [continue_txt_rect[0], continue_txt_rect[1]+50])
        
        self.clock.tick(SPEED)
        pygame.display.update()

    def play(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_d and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_a and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_w and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_s and self.direction != Direction.UP:
                    self.direction = Direction.DOWN
        
        self.move(self.direction)
        self.body.insert(0, self.head)

        if self.head == self.food:
            self.score += 1
            self.spawn_food()
        else:
            self.body.pop()
            
        game_over = False
        play_again = False
        if self.isCollision():
            game_over = True
            self.end_game_screen()
            while True:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        play_again = True
                        return game_over, play_again
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        quit()

        self.update_screen()
        return game_over, play_again

if __name__ == '__main__':
    game = snake_game(SCREEN_WIDTH, SCREEN_HEIGHT)

    running = True
    while running:
        game_over, play_again = game.play()

        if game_over:
            running = False

        if game_over and play_again:
            running = True
            game = snake_game(SCREEN_WIDTH, SCREEN_HEIGHT)