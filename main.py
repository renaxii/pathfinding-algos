import pygame
import asyncio
from algorithms import bfs

pygame.init()

WIDTH = 800
HEIGHT = 640
ROWS = 16
COLS = 20
CELL_SIZE = WIDTH // COLS

WHITE = (245, 245, 245)
BLACK = (30, 35, 45)
GREEN = (80, 190, 120)
RED = (220, 90, 90)
BLUE = (130, 190, 230)
YELLOW = (245, 210, 100)
GRID_COLOR = (190, 195, 200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("title placeholder")

# False = empty, True = wall
grid = [[False for _ in range(COLS)] for _ in range(ROWS)]

start = (1, 1)
end = (14, 18)

animation_order = []
animation_index = 0

explored = set()
final_path = []
path_cells = set()

frame_counter = 0
animating = False

# dragging variables
moving_start = False
moving_end = False
wall_mode = None

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


def edit_wall(cell, make_wall):
    row, col = cell

    if cell == start or cell == end:
        return

    if grid[row][col] != make_wall:
        grid[row][col] = make_wall
        reset_search()


def draw_grid():
    screen.fill(WHITE)

    for row in range(ROWS):
        for col in range(COLS):

            x = col * CELL_SIZE
            y = row * CELL_SIZE
            cell = (row, col)

            color = WHITE

            if grid[row][col]:
                color = BLACK

            elif cell in explored:
                color = BLUE

            # path found
            if cell in path_cells:
                color = YELLOW

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

    if 0 <= row < ROWS and 0 <= col < COLS:
        return (row, col)
    return None


async def main():
    global start, end
    global moving_start, moving_end, wall_mode
    global animation_order, animation_index
    global explored, final_path, path_cells
    global frame_counter, animating

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                cell = get_cell(event.pos)

                if cell is not None and event.button == 1:

                    if cell == start:
                        moving_start = True
                        wall_mode = None

                    elif cell == end:
                        moving_end = True
                        wall_mode = None

                    else:
                        wall_mode = not grid[cell[0]][cell[1]]
                        edit_wall(cell, wall_mode)

            if event.type == pygame.MOUSEMOTION:
                cell = get_cell(event.pos)

                if cell is not None:
                    buttons = pygame.mouse.get_pressed()

                    if moving_start and buttons[0]:
                        if not grid[cell[0]][cell[1]] and cell != end:
                            start = cell
                            reset_search()

                    elif moving_end and buttons[0]:
                        if not grid[cell[0]][cell[1]] and cell != start:
                            end = cell
                            reset_search()

                    elif wall_mode is not None and buttons[0]:
                        edit_wall(cell, wall_mode)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    moving_start = False
                    moving_end = False
                    wall_mode = None

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

        draw_grid()
        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())