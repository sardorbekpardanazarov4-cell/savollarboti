import pygame
import random
import sys


CELL_SIZE = 20    
COLS = 30           
ROWS = 20           
WIDTH = CELL_SIZE * COLS
HEIGHT = CELL_SIZE * ROWS
FPS = 5           

# Ranglar (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (40, 40, 40)

# --- Pygame boshlash ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake o'yini — Sardor uchun")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# --- Yordamchi funksiyalar ---
def draw_block(color, pos):
    """Katakka rang berib chizadi. pos = (x, y) katak indekslari"""
    rect = pygame.Rect(pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)

def random_food_position(snake):
    """Ilonga tegmagan tasodifiy ovqat joyi topadi"""
    while True:
        x = random.randint(0, COLS-1)
        y = random.randint(0, ROWS-1)
        if (x, y) not in snake:
            return (x, y)

def draw_grid():
    """Ixtiyoriy: tor grid chizadi (ko'rinish uchun)"""
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x,0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0,y), (WIDTH, y))


def new_game():
    start_x = COLS // 2
    start_y = ROWS // 2
    snake = [(start_x, start_y), (start_x-1, start_y), (start_x-2, start_y)]
    direction = (1, 0)  
    food = random_food_position(snake)
    score = 0
    return snake, direction, food, score

snake, direction, food, score = new_game()
game_over = False


while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            
            if event.key in (pygame.K_UP, pygame.K_w):
                if direction != (0, 1): direction = (0, -1)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                if direction != (0, -1): direction = (0, 1)
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                if direction != (1, 0): direction = (-1, 0)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                if direction != (-1, 0): direction = (1, 0)
            elif event.key == pygame.K_r and game_over:
                
                snake, direction, food, score = new_game()
                game_over = False

    if not game_over:
        
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        
        
        if (new_head[0] < 0 or new_head[0] >= COLS or
            new_head[1] < 0 or new_head[1] >= ROWS):
            game_over = True
        else:
            
            if new_head in snake:
                game_over = True
            else:
                snake.insert(0, new_head) 
                
                if new_head == food:
                    score += 1
                    food = random_food_position(snake)
                    
                    if score % 5 == 0:
                        FPS = int(FPS * 1.1)  
                else:
                    snake.pop()  

    
    screen.fill(BLACK)
    draw_grid()

    
    draw_block(RED, food)

    
    for i, segment in enumerate(snake):
        color = GREEN if i == 0 else (0, 155, 0)
        draw_block(color, segment)

    
    score_surf = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surf, (10, 10))

    if game_over:
        over_surf = font.render("Game Over! R - restart", True, WHITE)
        
        rect = over_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(over_surf, rect)

    pygame.display.flip()
    clock.tick(FPS)
