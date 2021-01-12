from typing import Callable, TypeVar, List, Optional, NamedTuple
from enum import Enum
import random as rnd
from math import sqrt
from skimage.io import imshow
from matplotlib import pyplot as plt
from visual_map import *
from maze_generation.make_perlin import make_perlin_field
from maze_generation.perlin_to_color import make_polygon_colored, rgb


# all statuses
class Cell(str, Enum):
    EMPTY = " "
    BLOCKED = "X"
    START = "S"
    GOAL = "G"
    PATH = "*"


# store the location of cell
class MazeLocation(NamedTuple):
    row: int
    col: int


class Maze:
    def __init__(self, dim: int = 20, sparseness: float = 0.2, start: MazeLocation = MazeLocation(0, 0),
                 goal: MazeLocation = MazeLocation(59, 59)) -> None:

        # handle of the start cell and of the goal cell
        start: MazeLocation = Maze._handle_key_cell(dim, start)
        goal: MazeLocation = Maze._handle_key_cell(dim, goal)

        self._dim: int = dim
        self.start: MazeLocation = start
        self.goal: MazeLocation = goal

        # init field
        self._grid: List[List[Cell]] = [[Cell.EMPTY for c in range(dim)] for r in range(dim)]

        # init perlin map for field
        self.perlin_markup = make_polygon_colored(make_perlin_field(dim // 10, 10))

        # make random blocked cells
        self._randomly_fill(dim, dim, sparseness)

        # assign start cell
        self._grid[start.row][start.col] = Cell.START

        # assign stop cell
        self._grid[goal.row][goal.col] = Cell.GOAL

    # correct values of the start cell and of the goal cell
    @staticmethod
    def _handle_key_cell(size: int, cell: MazeLocation) -> MazeLocation:
        output: List[int] = [cell.row, cell.col]
        if cell.col < 0:
            output[1] = 0
        if cell.row < 0:
            output[0] = 0
        if cell.col > size:
            output[1] = size - 1
        if cell.row > size:
            output[0] = size - 1

        return MazeLocation(output[0], output[1])

    def _randomly_fill(self, rows: int, cols: int, sparseness: float) -> None:
        for r in range(rows):
            for c in range(cols):
                rand_val = rnd.uniform(-1, 1)
                if rand_val < sparseness:
                    self._grid[r][c] = Cell.BLOCKED

    def goal_test(self, ml: MazeLocation) -> bool:
        return self.goal == ml

    def successors(self, ml: MazeLocation) -> List[MazeLocation]:

        locations: List[MazeLocation] = []

        if ml.row + 1 < self._dim and self._grid[ml.row + 1][ml.col] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row + 1, ml.col))

        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.col] != Cell:
            locations.append(MazeLocation(ml.row - 1, ml.col))

        if ml.col + 1 < self._dim and self._grid[ml.row][ml.col + 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.col + 1))

        if ml.col - 1 >= 0 and self._grid[ml.row][ml.col - 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.col - 1))

        return locations

    def visual(self, win: Window) -> None:
        frame = MazeVisual(win, self._dim)
        frame.make_map(self.perlin_markup)
        frame.mark_start_goal(self.start, self.goal)

    def test(self) -> None:
        imshow(self.perlin_markup)
        plt.show()

    def cost(self, ml: MazeLocation) -> float:
        array_of_cost = (np.arange(len(rgb))) / 2
        cur_rgb = self.perlin_markup[ml.col][ml.row]
        ind_of_color = rgb.index(cur_rgb.tolist())

        return array_of_cost[ind_of_color]


if __name__ == "__main__":
    window = Window()
    maze = Maze(50)
    maze.test()
    maze.visual(window)
    window.mainloop()
