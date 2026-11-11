import random
from typing import Any 



NORTH: int = 1 << 0
EAST: int = 1 << 1
SOUTH: int = 1 << 2
WEST: int = 1 << 3



class Cell():
    _location: tuple[int, int] = (0, 0)
    walls: int = 15

    def __init__(self, row: int, col: int) -> None:
        self._location = (row, col)

    def get_adjacent_positions(self) -> list[tuple[int, int]]:
        result: list[tuple[int, int]] = []
        result.append((self._location[0], self._location[1] + 1))
        result.append((self._location[0] + 1, self._location[1]))
        result.append((self._location[0], self._location[1] - 1))
        result.append((self._location[0] - 1, self._location[1]))
        return result

    def get_position_direction(self, position: tuple[int, int]) -> int:
        positions: list[tuple[int, int]] = self.get_adjacent_positions()
        for i in range(len(positions)):
            if positions[i] == position:
                return 1 << i
        return 0

    def get_position(self) -> tuple[int, int]:
        return self._location
    
    def set_walls(self, direction: int) -> None:
        self._walls = self._walls | direction

    def check_walls(self, direction: int) -> bool:
        return ((self._walls & direction) > 0)

    def remove_walls(self, direction: int) -> None:
        direction = direction & self._walls
        self._walls = self._walls ^ direction

    def remove_wall(self, cell: Cell) -> None:
        self.remove_wall(self.get_position_direction(cell.get_position()))

    def check_wall(self, cell: Cell) -> bool:
        return self.check_walls(self.get_position_direction(cell.get_position()))


class MazeGenerator():
    _width: int = -1
    _height: int = -1
    _entry: tuple[int, int] = (0, 0)
    _exit: tuple[int, int] = (0, 0)
    _output_file: str = ""
    _perfect: bool = False
    _seed: int = -1
    grid: list[list[Cell]] = []


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
        self._seed: Any = random.Random(seed) if seed != None else random.Random()
        self.grid: list[list[Cell]] = []
        self.create_grid()


    def create_grid(self) -> None:
        for i in range(self._height):
            row: list[Cell] = []
            for j in range(self._width):
                row.append(Cell(i, j))
            self.grid.append(row)


    def is_ouside(self, pos: tuple[int, int]) -> bool:
        if pos[0] < 0 or pos[1] < 0:
            return True
        if pos[1] >= self._width or pos[0] >= self._height:
            return True
        return False

    def get_cell(self, pos: tuple[int, int]) -> Cell:
        return self._grid[pos[1]][pos[0]]

    def random_cell(self) -> Cell:
        return self.get_cell((random.randint(0, self._height),
            random.randint(0, self._width)))

    def get_adjacent_cells(self, cell: Cell) -> list[Cell]:
        adjacent_pos: list[tuple[int, int]] = cell.get_adjacent_positions(cell.get_position())
        return [pos if self.is_ouside() for pos in adjacent_pos]

    def get_possible_cells(self, cell: Cell) -> list[Cell]:
        return [c if not cell.check_wall(c) for c in self.get_adjacent_cells(cell)]

    def remove_wall(self, cel1: Cell, cel2: Cell) -> None:
        cel1.remove_wall(cel2)
        cel2.remove_wall(cel1)

    def generate_maze(self) -> None:
        queue: list[Cell] = []
        stepped: set[Cell] = set()
        queue.append(self.random_cell())

        while len(queue) > 0:
            chosen: Cell = random.choice(queue)
            queue.remove(chosen)
            if len(stepped) != 0:
                wall: Cell = random.choice([cell if cell in stepped for cell in self.get_adjacent_cells(chosen)])
            stepped.add(chosen)
            self.remove_wall(chosen, wall)

            for i in chosen.get_adjacent_cells(chosen):
                if not i in stepped:
                    queue.add(i)

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
