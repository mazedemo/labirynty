import numpy as np
import random
from graphics import *

x_size = int(input("Podaj szerokość labiryntu: "))
y_size = int(input("Podaj wysokość labiryntu: "))

STEP = 2
CELL_SIZE = 40
FRAME_RATE = 4

def clear(win):
    for item in win.items[:]:
        item.undraw()

def redraw(win, maze, framerate):
    clear(win)
    print_maze_graph(win, maze)
    update(framerate)

def clear_maze(cells):
    for y in range(0, cells.shape[1]):
        for x in range(0, cells.shape[0]):
            cells[x, y] = ' '

def fill_maze(cells):
    for y in range(0, cells.shape[1]):
        for x in range(0, cells.shape[0]):
            if x % 2 != 0 and y % 2 == 0:
                cells[x, y] = 'W'
            elif x % 2 == 0 and y % 2 != 0:
                cells[x, y] = 'W'
            else:
                cells[x, y] = ' '

def print_maze_graph(win, cells):
    pt_up_left = Point(0, 0)
    pt_up_right = Point(x_size*CELL_SIZE, 0)
    pt_down_left = Point(0, y_size*CELL_SIZE)
    pt_down_right = Point(x_size*CELL_SIZE, y_size * CELL_SIZE)
    ln = Line(pt_up_left, pt_up_right)
    ln.setOutline(color_rgb(0, 255, 255))
    ln.draw(win)

    ln = Line(pt_up_right, pt_down_right)
    ln.setOutline(color_rgb(0, 255, 255))
    ln.draw(win)

    ln = Line(pt_down_right, pt_down_left)
    ln.setOutline(color_rgb(0, 255, 255))
    ln.draw(win)

    ln = Line(pt_down_left, pt_up_left)
    ln.setOutline(color_rgb(0, 255, 255))
    ln.draw(win)

    for y in range(0, cells.shape[1]):
        for x in range(0, cells.shape[0]):
            if cells[x, y] == ' ':
                continue
            if x % 2 != 0 and y % 2 == 0:
                pt1 = Point((x//2+1)*CELL_SIZE, (y//2)*CELL_SIZE)
                pt2 = Point((x//2+1)*CELL_SIZE, (y//2+1)*CELL_SIZE)
                ln = Line(pt1, pt2)
                if cells[x, y] == 'C':
                    ln.setOutline('red')
                else:
                    ln.setOutline(color_rgb(0, 255, 255))
                ln.draw(win)
            elif x % 2 == 0 and y % 2 != 0:
                pt1 = Point((x//2)*CELL_SIZE, (y//2+1)*CELL_SIZE)
                pt2 = Point((x//2+1)*CELL_SIZE, (y//2+1)*CELL_SIZE)
                ln = Line(pt1, pt2)
                if cells[x, y] == 'C':
                    ln.setOutline('red')
                else:
                    ln.setOutline(color_rgb(0, 255, 255))
                ln.draw(win)
            elif x % 2 == 0 and y % 2 == 0:
                pt1 = Point((x // 2) * CELL_SIZE+1, (y // 2) * CELL_SIZE+1)
                pt2 = Point((x // 2 + 1) * CELL_SIZE-1, (y // 2 + 1) * CELL_SIZE-1)
                rt = Rectangle(pt1, pt2)
                if cells[x, y] == 'C':
                    #rt.setOutline(color_rgb(0, 255, 0))
                    rt.setFill(color_rgb(0, 56, 0))
                    rt.draw(win)
                else:
                    try:
                        str(cells[x, y])
                    except ValueError:
                        continue
                    pt1.move(CELL_SIZE/2, CELL_SIZE/2)
                    label = Text(pt1, cells[x, y])
                    color = color_rgb(hash(cells[x, y]) % 256, hash(cells[x, y] + "1") % 256, hash(cells[x, y] + "2") % 256)
                    label.setOutline(color)
                    label.setFill(color)
                    label.setSize(CELL_SIZE//3)
                    label.draw(win)

def get_cell(cells, x, y):
    return cells[x*STEP-2, y*STEP-2]

def get_cell_not_visited_neighbours(cells, x, y):
    neighbours = []
    if x > 1:
        neighbour = get_cell(cells, x-1, y)
        if neighbour != 'V':
            neighbours.append([x-1, y])
    if x < x_size:
        neighbour = get_cell(cells, x+1, y)
        if neighbour != 'V':
            neighbours.append([x+1, y])
    if y > 1:
        neighbour = get_cell(cells, x, y-1)
        if neighbour != 'V':
            neighbours.append([x, y-1])
    if y < y_size:
        neighbour = get_cell(cells, x, y+1)
        if neighbour != 'V':
            neighbours.append([x, y+1])
    return neighbours

def set_cell(cells, x, y, value):
    cells[x*STEP-2, y*STEP-2] = value

def set_wall(cells, x1, y1, x2, y2, value):
    if x1 != x2 and y1 != y2:
        print("ERROR: Column xor row must be the same")
        return
    if abs(x1-x2) > 1 or abs(y1-y2) > 1:
        print("ERROR: Cells must be neighbours")
        return

    if x1 - x2 < 0:
        cells[x1*STEP-1, y1*STEP-2] = value
    elif x1 - x2 > 0:
        cells[x2*STEP-1, y2*STEP-2] = value
    elif y1 - y2 < 0:
        cells[x1*STEP-2, y1*STEP-1] = value
    else:
        cells[x2*STEP-2, y2*STEP-1] = value

def recursive_backtracker(win, maze):
    visited_stack = []

    init_x = random.randint(1, x_size)
    init_y = random.randint(1, y_size)

    visited_stack.append([init_x, init_y])
    set_cell(maze, init_x, init_y, 'V')

    while visited_stack:
        current_cell = visited_stack.pop()
        set_cell(maze, current_cell[0], current_cell[1], 'C')
        neighbours = get_cell_not_visited_neighbours(maze, current_cell[0], current_cell[1])
        if not neighbours:
            redraw(win, maze, FRAME_RATE)
            set_cell(maze, current_cell[0], current_cell[1], 'V')
            continue
        visited_stack.append(current_cell)
        chosen_neighbour = random.choice(neighbours)
        set_wall(maze, current_cell[0], current_cell[1], chosen_neighbour[0], chosen_neighbour[1], 'C')
        set_cell(maze, chosen_neighbour[0], chosen_neighbour[1], 'V')
        visited_stack.append(chosen_neighbour)

        redraw(win, maze, FRAME_RATE)
        set_wall(maze, current_cell[0], current_cell[1], chosen_neighbour[0], chosen_neighbour[1], ' ')
        set_cell(maze, current_cell[0], current_cell[1], 'V')

# raw maze, filled with 0's
maze = np.zeros(shape=(x_size*2-1, y_size*2-1)).astype(str)

win = GraphWin("ss", x_size*CELL_SIZE+1, y_size*CELL_SIZE+1, autoflush=False)
win.setBackground(color_rgb(0, 0, 0))

random.seed(a=3)

clear_maze(maze)
fill_maze(maze)
recursive_backtracker(win, maze)

redraw(win, maze, FRAME_RATE)

win.getMouse()
win.close()
