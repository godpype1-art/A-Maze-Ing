
import random

class Cell():
    _location: tuple[int, int] = (0, 0)
    _walls: int = 15

    def __init__(self, x: int, y: int) -> None:
        self._location = (x, y)

    def get_adjacent_positions(self) -> list[tuple[int, int]]:
        result: list[tuple[int, int]] = []
        result.append((self._location[0], self._location[1] + 1))
        result.append((self._location[0] + 1, self._location[1]))
        result.append((self._location[0], self._location[1] - 1))
        result.append((self._location[0] - 1, self._location[1]))
        return result


class MazeGenerator():
    _width: int = -1
    _height: int = -1
    _entry: tuple[int, int] = (0, 0)
    _exit: tuple[int, int] = (0, 0)
    _output_file: str = ""
    _perfect: bool = False
    _seed: int = -1
    _grid: list[list[Cell]] = []


    def __init__(
            self,
            width: int,
            height: int,
            entry: tuple[int, int],
            exit: tuple[int, int],
            output: str,
            perfect: bool,
            seed: int | None = None
            ) -> None:
        self._width: int = width
        self._height: int = height
        self._entry: tuple[int, int] = entry
        self._exit: tuple[int, int] = exit
        self._output_file: str = output
        self._perfect: bool = perfect
        self._seed: int = seed

    def create_grid(self) -> None:
        for i in range(self._width):
            col: list[Cell] = []
            for j in range(self._height):
                cell = Cell(i, j)
                col.append(cell)
            self._grid.append(col)

    def is_ouside(self, pos: tuple[int, int]) -> bool:
        if pos[0] < 0 or pos[1] < 0:
            return True
        if pos[0] >= self._width or pos[1] >= self._height:
            return True
        return False

    def random_cell(self) -> Cell:
        return self._grid[random.randint(0, self._height)][
            random.randint(0, self._width)]

    def get_adjacent_cells(self, cell: Cell) -> list[Cell]:
        adjacent_pos: list[tuple[int, int]] = cell.get_adjacent_positions()
        result: list[Cell] = []


    def generate_maze(self) -> None:
        queue: list[Cell] = []
        stepped: set[Cell] = set()
        queue.append(self.random_cell())

        while len(queue) > 0:
            chosen: Cell = random.choice(queue)
            stepped.add(chosen)
            queue.remove(chosen)
            for i in chosen.get_adjacent_positions():
                if self._grid[]

    def show(self) -> None:
        print(
            "============= MAZE DATA ==============",
            "",
            "Data colected:",
            f"  Width: {self._width}",
            f"  Height: {self._height}",
            f"  Entry: {self._entry}",
            f"  Exit: {self._exit}",
            f"  Output File: {self._output_file}",
            f"  Perfect: {self._perfect}",
            f"  Seed: {self._seed}",
            sep="\n"
            )
