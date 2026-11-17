import pygame
from algorithms import bfs

pygame.init()

WIDTH  = 800
HEIGHT = 640
ROWS = 16
COLS = 20
CELL_SIZE = WIDTH // COLS

WHITE = (245,245,245)
BLACK = (30,35,45)
GREEN = (80,190,120)
RED = (220,90,90)
GRID_COLOR = (190,195,200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("title")
clock = pygame.time.Clock()

# false = empty; true = wall
grid = [[False for _ in range(COLS)] for _ in range(ROWS)]

start = (1,1)
end = (14,18)

def draw_grid():
    screen.fill(WHITE)

    for row in range(ROWS):
        for col in range(COLS):

            x=col*CELL_SIZE
            y=row*CELL_SIZE

            # default
            color = WHITE

            # wall
            if grid[row][col]:
                color = BLACK

            # start and end
            if (row, col) == start:
                color = GREEN
            elif (row, col) == end:
                color = RED

            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

            # grid lines
            pygame.draw.rect(screen, GRID_COLOR, (x, y, CELL_SIZE, CELL_SIZE), 1)

def place_wall(mouse_pos):
    x, y = mouse_pos

    col = x // CELL_SIZE
    row = y // CELL_SIZE

    if 0<= row < ROWS and 0 <= col < COLS:
        if (row, col) != start and (row, col) != end:
            grid[row][col] = True


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            col = mouse_x // CELL_SIZE
            row = mouse_y // CELL_SIZE

            if 0<=row<ROWS and 0<=col<COLS:
                if (row, col) != start and (row, col) != end:

                    # left click = add wall
                    if event.button==1:
                        grid[row][col] = True

                    # right click = remove wall
                    elif event.button==3:
                        grid[row][col] = False

        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            col = mouse_x // CELL_SIZE
            row = mouse_y // CELL_SIZE

            if 0<=row<ROWS and 0<=col<COLS:
                if (row, col) != start and (row,col) != end:
                    # left mouse -> draw
                    if pygame.mouse.get_pressed()[0]:
                            grid[row][col] = True

                    # right mouse -> erase
                    elif pygame.mouse.get_pressed()[2]:
                        grid[row][col] = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                visited, path = bfs(grid, start, end)

                print("Visited cells:", len(visited))
                print("Shortest path length:", len(path))
    
    draw_grid()

    pygame.display.update()
    clock.tick(60)

pygame.quit()

if __name__ == "__main__":
    main()