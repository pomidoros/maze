from tkinter import *
from maze_generation.make_perlin import *
from math import floor
from typing import Callable, List, Generic, TypeVar
import numpy as np


# Location
L = TypeVar('L')
# Perlin array
P = TypeVar('P')


# create a window
class Window(Tk):
    def __init__(self, width: int = 800, height: int = 800) -> None:
        super().__init__()
        # size of the window
        self.geometry("{w}x{h}".format(w=str(width), h=str(height)))
        self.width: int = width
        self.height: int = height
        self.resizable(0, 0)
        self.title("Map")


class MazeVisual(Generic[L, P], Frame):
    def __init__(self, win: Window, dim: int) -> None:
        # create a Frame from Window
        super().__init__(master=win)
        # size of frame is a square
        self.size: int = min(win.height, win.width)
        # the dimension of maze
        self.dim = dim
        # the size of cell
        self.dx = floor(self.size / self.dim)
        self.pack(fill=BOTH, expand=1)
        self._init_UI()

    def _init_UI(self) -> None:
        self.canvas = Canvas(master=self, bg="white")
        self.canvas.pack(fill=BOTH, expand=1)

    # take the perlin map
    def make_map(self, arr: P):
        # visual of all cells
        for i in range(self.dim):
            for j in range(self.dim):
                # take RGB-format
                r = arr[i][j][0]
                g = arr[i][j][1]
                b = arr[i][j][2]
                # convert to RGB-style
                res_color = f'#{r:02x}{g:02x}{b:02x}'
                # make cell
                self.canvas.create_rectangle(j * self.dx, i * self.dx, (j + 1) * self.dx,
                                             (i + 1) * self.dx, fill=res_color)

    def mark_start_goal(self, start: L, goal: L) -> None:
        self.canvas.create_rectangle(start.row * self.dx, start.col * self.dx,
                                     (start.row + 1) * self.dx, (start.col + 1) * self.dx,
                                     fill="brown")
        self.canvas.create_rectangle(goal.row * self.dx, goal.col * self.dx,
                                     (goal.row + 1) * self.dx, (goal.col + 1) * self.dx,
                                     fill="brown")

