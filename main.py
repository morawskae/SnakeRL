import pygame
from enum import Enum
import random

CELL_HEIGHT:int = 30
CELL_WIDTH:int = 30
CELLS_PER_ROW = 20
ROWS_PER_SCREEN=16

class Direction(Enum):
    UP=1
    DOWN=2
    LEFT=3
    RIGHT=4

def render_board(cell_height, cell_width, cells_per_row, rows_per_screen, screen,snake_body,apple_arr):
    
    for i in range (cells_per_row):
        for j in range(rows_per_screen):
            if ([i,j] in snake_body):
                pygame.draw.rect(screen,pygame.Color(83,115,36),(i*(cell_width),j*(cell_height), cell_width,cell_height))
            if([i,j] in apple_arr):
                pygame.draw.rect(screen,pygame.Color(237,38,38),(i*(cell_width),j*(cell_height), cell_width,cell_height))
            pygame.draw.rect(screen,"black",(i*(cell_width),j*(cell_height), cell_width,cell_height),width=1)  

def update_pos_arr(direction:Direction,snake_body:list, apple_arr:list):

    head= snake_body[0].copy()
    match direction:
        case Direction.UP:
            head[1]-=1
        case Direction.DOWN:
            head[1]+=1
        case Direction.LEFT:
            head[0]-=1
        case Direction.RIGHT:
            head[0]+=1

    #rozbij dla komunikatow
    if((head in snake_body[1::]) or (head[1]<0 or head[1]>=ROWS_PER_SCREEN) or (head[0]<0 or head[0]>=CELLS_PER_ROW)):
        return False
    if head in apple_arr:
        apple_arr.remove(head)
    else:
        snake_body.pop()
    snake_body.insert(0,head) 
    return True

def spawn_apple(apple_arr:list, snake_body: list):
    if len(apple_arr)!=0:
        return
    if random.random() <=0.05:
        pot_coord = [random.randint(0,CELLS_PER_ROW-1),random.randint(0,ROWS_PER_SCREEN-1)]
        if(pot_coord not in snake_body):
            apple_arr.append(pot_coord)

pygame.init()
screen = pygame.display.set_mode((CELL_WIDTH*CELLS_PER_ROW,CELL_HEIGHT*ROWS_PER_SCREEN))
clock = pygame.time.Clock()
running= True

move_delay = 100
last_move = pygame.time.get_ticks()
max_fps=60

#init snake_body

snake_body = [[CELLS_PER_ROW//2,ROWS_PER_SCREEN//2]]
apple_arr = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(pygame.Color(162,199,105))
    #render here
    render_board(CELL_HEIGHT,CELL_WIDTH,CELLS_PER_ROW,ROWS_PER_SCREEN,screen,snake_body,apple_arr)

    now = pygame.time.get_ticks()

    if now - last_move >=move_delay:
        spawn_apple(apple_arr,snake_body)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            running = update_pos_arr(Direction.UP,snake_body,apple_arr)
        elif keys[pygame.K_s]:
            running = update_pos_arr(Direction.DOWN,snake_body,apple_arr)
        elif keys[pygame.K_a]:
            running = update_pos_arr(Direction.LEFT,snake_body,apple_arr)
        elif keys[pygame.K_d]:
            running = update_pos_arr(Direction.RIGHT,snake_body,apple_arr)
        last_move = now

    #print(snake_body)
    pygame.display.flip()
    clock.tick(max_fps)

pygame.quit()