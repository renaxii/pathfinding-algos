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
BLUE = (130, 190, 230)
YELLOW = (245, 210, 100)
GRID_COLOR = (190,195,200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("title")
clock = pygame.time.Clock()

# false = empty; true = wall
grid = [[False for _ in range(COLS)] for _ in range(ROWS)]

start = (1,1)
end = (14,18)

animation_order = []
animation_index = 0

explored = set()
final_path = []
path_cells = set()

frame_counter = 0
animating = False

moving_start = False
moving_end = False

def reset_search():
    global animation_order, animation_index
    global explored, final_path, path_cells
    global frame_counter, animating

    animation_order = []
    animation_index = 0
    explored.clear()
    final_path = []
    path_cells.clear()
    frame_counter = 0
    animating = False

def draw_grid():
    screen.fill(WHITE)

    for row in range(ROWS):
        for col in range(COLS):

            x = col * CELL_SIZE
            y = row * CELL_SIZE
            cell = (row, col)

            # default
            color = WHITE

            # wall
            if grid[row][col]:
                color = BLACK
            elif cell in explored:
                color = BLUE

            # path
            if cell in path_cells:
                color = YELLOW

            # start and end
            if cell == start:
                color = GREEN
            elif cell == end:
                color = RED

            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRID_COLOR, (x, y, CELL_SIZE, CELL_SIZE), 1)

def get_cell(mouse_pos):
    x, y = mouse_pos

    col = x // CELL_SIZE
    row = y // CELL_SIZE

    if 0<= row < ROWS and 0 <= col < COLS:
        return (row, col)
    else:
        return None

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
            cell = get_cell(event.pos)

            if cell is not None:
                if event.button == 1:
                    if cell == start:
                        moving_start = True
                    elif cell != end:
                        grid[cell[0]][cell[1]] = True
                        reset_search()

                elif event.button == 3:
                    if cell == end:
                        moving_end = True
                    elif cell != start:
                        grid[cell[0]][cell[1]] = False
                        reset_search()

        if event.type == pygame.MOUSEMOTION:
            cell = get_cell(event.pos)

            if cell is not None:
                buttons = pygame.mouse.get_pressed()

                if moving_start and buttons[0]:
                    if not grid[cell[0]][cell[1]] and cell != end:
                        start = cell
                        reset_search()

                elif moving_end and buttons[2]:
                    if not grid[cell[0]][cell[1]] and cell != start:
                        end = cell
                        reset_search()

                elif buttons[0]:
                    if cell != start and cell != end:
                        grid[cell[0]][cell[1]] = True
                        reset_search()

                elif buttons[2]:
                    if cell != start and cell != end:
                        grid[cell[0]][cell[1]] = False
                        reset_search()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                moving_start = False

            elif event.button == 3:
                moving_end = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                animation_order, final_path = bfs(grid, start, end)

                animation_index = 0
                explored = set()
                path_cells = set()
                frame_counter = 0

                animating = True

                print("Visited cells:", len(animation_order))
                print("Path length:", len(final_path))

                if not final_path:
                    print("No path found!")

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                moving_start = False
            elif event.button == 3:
                moving_end = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                animation_order, final_path = bfs(grid, start, end)

                animation_index = 0
                explored = set()
                path_cells = set()
                frame_counter = 0

                animating = True

                print("Visited cells:", len(animation_order))
                print("Path length:", len(final_path))

                if not final_path:
                    print("No path found!")

    # Animate BFS
    if animating:
        frame_counter += 1

        if frame_counter >= 3:
            frame_counter = 0

            if animation_index < len(animation_order):
                explored.add(animation_order[animation_index])
                animation_index += 1

            else:
                animating = False
                path_cells = set(final_path)

    # Draw the grid EVERY frame
    draw_grid()

    pygame.display.update()
    clock.tick(60)

pygame.quit()