
import random


class Maze():
    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int], output: str, perfect: bool) -> None:
        self._width: int = width
        self._height: int = height
        self._entry: tuple[int, int] = entry
        self._exit: tuple[int, int] = exit
        self._output: str = output
        self._perfect: bool = perfect
        self.generate_maze()

    def init_initial_maze(self) -> None:
        row: list[int] = []
        self._maze: list[list[int]] = []
        for rw in range(self._height):
            for tt in range(self._width):
                row.append(15)
            self._maze.append(row.copy())
            row = []

    def generate_maze(self):
        queue: list[int] = []
        self.init_initial_maze()

