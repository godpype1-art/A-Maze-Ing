import random
from typing import Any


NORTH: int = 1 << 0
EAST: int = 1 << 1
SOUTH: int = 1 << 2
WEST: int = 1 << 3


class Cell():
    _location: tuple[int, int] = (0, 0)
    _walls: int = 15

    def __init__(self, col: int, row: int) -> None:
        self._location = (col, row)

    def get_adjacent_positions(self) -> list[tuple[int, int]]:
        result: list[tuple[int, int]] = []
        result.append((self._location[0], self._location[1] - 1))
        result.append((self._location[0] + 1, self._location[1]))
        result.append((self._location[0], self._location[1] + 1))
        result.append((self._location[0] - 1, self._location[1]))
        return result

    def get_position_direction(self, position: tuple[int, int]) -> int:
        positions: list[tuple[int, int]] = self.get_adjacent_positions()
        for i in range(len(positions)):
            if positions[i] == position:
                return 1 << i
        return 0

    def get_cell_direction(self, cell: "Cell") -> int:
        return self.get_position_direction(cell.get_position())

    def get_position(self) -> tuple[int, int]:
        return self._location

    def set_walls(self, direction: int) -> None:
        self._walls = self._walls | direction

    def check_walls(self, direction: int) -> bool:
        return ((self._walls & direction) > 0)

    def remove_walls(self, direction: int) -> None:
        direction = direction & self._walls
        self._walls = self._walls ^ direction

    def remove_wall(self, cell: "Cell") -> None:
        self.remove_walls(self.get_position_direction(cell.get_position()))

    def check_wall(self, cell: "Cell") -> bool:
        return self.check_walls(self.get_position_direction(
                                cell.get_position()))

    def get_location(self) -> tuple[int, int]:
        return self._location

    def get_hexadecimal(self) -> str:
        return hex(self._walls).removeprefix("0x")

    def __str__(self):
        return f"Cell{self._location}"


class CellPath():
    _size: int = 0
    _rest: Any | None = None

    def __init__(self, start: Cell, before: Any | None = None) -> None:
        self._head: Cell = start

        if before is not None:
            self._rest = before

            self._size: int = 1 + before.get_size()

    def get_size(self) -> int:
        return self._size

    def branch(self, new_place: Cell) -> "CellPath":
        return CellPath(new_place, self)

    def generate_branchs(self, nodes: list[Cell]) -> list["CellPath"]:
        result: list[CellPath] = []
        for node in nodes:
            result.append(self.branch(node))
        return result

    def get_head(self) -> Cell:
        return self._head

    def get_head_direction(self) -> int:
        if self._size == 1 or self._rest is None:
            return 0
        return self._head.get_cell_direction(self._rest.get_head())

    def __str__(self) -> str:
        direction: int = self.get_head_direction()
        if direction == NORTH:
            return str(self._rest) + "N"
        if direction == EAST:
            return str(self._rest) + "E"
        if direction == WEST:
            return str(self._rest) + "W"
        if direction == SOUTH:
            return str(self._rest) + "S"
        return ""


class MazeGenerator():
    _width: int = -1
    _height: int = -1
    _entry: tuple[int, int] = (0, 0)
    _exit: tuple[int, int] = (0, 0)
    _output_file: str = ""
    _perfect: bool = False
    _seed: int = -1
    _maze_random: random.Random = random.Random()
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

        if seed is not None:
            self._seed = seed
            self._maze_random: random.Random = random.Random(seed)

        self._grid: list[list[Cell]] = []
        self._answer: CellPath | None = None

        self.create_grid()
        self._cell_exit: Cell = self.get_cell(self._exit)
        self._cell_entry: Cell = self.get_cell(self._entry)

    def create_grid(self) -> None:
        for i in range(self._height):
            row: list[Cell] = []
            for j in range(self._width):
                row.append(Cell(j, i))
            self._grid.append(row)

    def is_ouside(self, pos: tuple[int, int]) -> bool:
        if pos[0] < 0 or pos[1] < 0:
            return True
        if pos[1] >= self._height or pos[0] >= self._width:
            return True
        return False

    def get_cell(self, pos: tuple[int, int]) -> Cell:
        return self._grid[pos[1]][pos[0]]

    def random_cell(self) -> Cell:
        return self.get_cell((self._maze_random.randint(0, self._width - 1),
                              self._maze_random.randint(0, self._height - 1)))

    def get_adjacent_cells(self, cell: Cell) -> list[Cell]:
        adjacent_pos: list[tuple[int, int]] = cell.get_adjacent_positions()
        return [self.get_cell(pos) for pos in adjacent_pos if not self.is_ouside(pos)]

    def get_possible_cells(self, cell: Cell) -> list[Cell]:
        return [c for c in self.get_adjacent_cells(cell) if not cell.check_wall(c)]

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

            if len(stepped) > 0:
                wall: Cell = self._maze_random.choice([cell for cell in self.get_adjacent_cells(chosen) if cell in stepped])
                self.remove_wall(chosen, wall)

            stepped.add(chosen)

            for i in self.get_adjacent_cells(chosen):
                if i not in stepped and i not in queue:
                    queue.append(i)

    def solve_maze(self) -> None:
        queue: list[CellPath] = []
        stepped: set[Cell] = set()
        queue.append(CellPath(self._cell_entry))

        while len(queue) > 0:
            chosen: CellPath = queue[0]
            chosen_head: Cell = chosen.get_head()

            queue.remove(chosen)
            stepped.add(chosen.get_head())

            for i in self.get_possible_cells(chosen_head):
                if i == self._cell_exit:
                    self._answer = chosen.branch(i)
                    break
                if i not in stepped:
                    queue.append(chosen.branch(i))

    def save_as_file(self) -> None:
        with open(self._output_file, "w") as file:
            for line in self._grid:
                for node in line:
                    file.write(node.get_hexadecimal())
                file.write("\n")

            file.write("\n")

            file.write(f"{self._entry[0]},{self._entry[1]}\n")
            file.write(f"{self._exit[0]},{self._exit[1]}\n")

            if self._answer is not None:
                file.write(str(self._answer))

    def execute(self) -> None:
        self.generate_maze()
        self.solve_maze()
        self.save_as_file()

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
