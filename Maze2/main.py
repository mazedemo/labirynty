import random
import maze
import maze_generator

x_size = int(input("Podaj szerokość labiryntu: "))
y_size = int(input("Podaj wysokość labiryntu: "))

maze_object = maze.Maze(x_size, y_size)
maze_graphics = maze.MazeGraphics(x_size, y_size)

random.seed(a=3)

maze_object.clear()
maze_object.fill()

maze_generator.recursive_backtracker(maze_graphics, maze_object)

maze_graphics.redraw(maze_object)
maze_graphics.destroy()
