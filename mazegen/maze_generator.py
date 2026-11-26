import random
from typing import Any
from .exceptions import MazeConfigError


NORTH: int = 1 << 0
EAST: int = 1 << 1
SOUTH: int = 1 << 2
WEST: int = 1 << 3


FORTY_TWO: list[tuple[int, int]] = [
    (0,0), (0,1), (0,2),
    (1,2), (2,2), (2,3),
    (2,4), (4,0), (5,0),
    (6,0), (6,1), (6,2),
    (5,2), (4,2), (4,3),
    (4,4), (5,4), (6,4)
    ]

class Cell():
    """A maze cell whose walls are kept as a bitmask.

    Each bit follows the ``NORTH``, ``EAST``, ``SOUTH`` and ``WEST``
    flags, and a set bit means that the wall exists. A new cell has
    its four walls. The ``_is_42``, ``_entry`` and ``_exit`` flags
    mark the special cells.
    """

    _location: tuple[int, int] = (0, 0)
    _walls: int = 15
    _is_42: bool = False
    _entry: bool = False
    _exit: bool = False

    def __init__(self, col: int, row: int) -> None:
        """Create a closed cell at column ``col`` and row ``row``."""
        self._location = (col, row)

    def get_adjacent_positions(self) -> list[tuple[int, int]]:
        """Return the neighbouring positions as ``(col, row)`` tuples.

        The order is north, east, south, west, the same as the direction
        flags. The positions may lie outside the maze.
        """
        result: list[tuple[int, int]] = []
        result.append((self._location[0], self._location[1] - 1))
        result.append((self._location[0] + 1, self._location[1]))
        result.append((self._location[0], self._location[1] + 1))
        result.append((self._location[0] - 1, self._location[1]))
        return result

    def get_position_direction(self, position: tuple[int, int]) -> int:
        """Return the direction flag from this cell towards ``position``.

        Return 0 if ``position`` is not adjacent to the cell.
        """
        positions: list[tuple[int, int]] = self.get_adjacent_positions()
        for i in range(len(positions)):
            if positions[i] == position:
                return 1 << i
        return 0

    def get_cell_direction(self, cell: "Cell") -> int:
        """Return the direction flag from this cell towards ``cell``.

        See ``get_position_direction``.
        """
        return self.get_position_direction(cell.get_position())

    def get_position(self) -> tuple[int, int]:
        """Return the ``(col, row)`` position of the cell."""
        return self._location

    def set_walls(self, direction: int) -> None:
        """Add the walls given by the ``direction`` flags."""
        self._walls = self._walls | direction

    def check_walls(self, direction: int) -> bool:
        """Return True if any wall given by ``direction`` exists."""
        return ((self._walls & direction) > 0)

    def remove_walls(self, direction: int) -> None:
        """Remove the walls given by the ``direction`` flags."""
        direction = direction & self._walls
        self._walls = self._walls ^ direction

    def remove_wall(self, cell: "Cell") -> None:
        """Remove the wall towards the adjacent ``cell``.

        Only the wall of this cell is removed. ``MazeGenerator.remove_wall``
        opens both sides.
        """
        self.remove_walls(self.get_position_direction(cell.get_position()))

    def check_wall(self, cell: "Cell") -> bool:
        """Return True if there is a wall towards the adjacent ``cell``."""
        return self.check_walls(self.get_position_direction(
                                cell.get_position()))

    def get_location(self) -> tuple[int, int]:
        """Return the ``(col, row)`` location, same as ``get_position``."""
        return self._location

    def get_hexadecimal(self) -> str:
        """Return the walls bitmask as one hexadecimal digit.

        It is the digit written to the output file. For example, ``9``
        means a wall to the north and a wall to the west.
        """
        return hex(self._walls).removeprefix("0x")

    def __str__(self):
        """Return the cell as text, for example ``Cell(2, 3)``."""
        return f"Cell{self._location}"

    def number_of_walls(self) -> int:
        """Return how many of the four walls the cell has."""
        return sum([1 for dir in [NORTH, WEST, EAST, SOUTH] if self.check_walls(dir)])

    def is_forty_two(self) -> bool:
        """Return True if the cell belongs to the 42 pattern."""
        return self._is_42

    def set_forty_two(self, valu: bool) -> None:
        """Mark whether the cell belongs to the 42 pattern."""
        self._is_42 = valu

    def is_entry(self) -> bool:
        """Return True if the cell is the maze entry."""
        return self._entry

    def is_exit(self) -> bool:
        """Return True if the cell is the maze exit."""
        return self._exit

    def get_walls(self) -> int:
        """Return the walls bitmask of the cell."""
        return self._walls


class CellPath():
    """A path through the maze, as an immutable linked list of cells.

    ``_head`` is the last cell of the path and ``_rest`` is the path
    that leads to it, so following ``_rest`` goes back to the start.
    ``_size`` counts the moves, which makes it 0 for a path with a
    single cell.
    """
    _size: int = 0
    _rest: Any | None = None

    def __init__(self, start: Cell, before: Any | None = None) -> None:
        """Create a path that ends at ``start``.

        Parameters
        ----------
        start : Cell
            Last cell of the new path.
        before : CellPath or None
            Path that is extended by ``start``. If it is ``None``, a new
            path with a single cell is started.
        """
        self._head: Cell = start

        if before is not None:
            self._rest = before

            self._size: int = 1 + before.get_size()

    def get_size(self) -> int:
        """Return the number of moves in the path."""
        return self._size

    def branch(self, new_place: Cell) -> "CellPath":
        """Return a new path that extends this one with ``new_place``.

        This path is left unchanged.
        """
        return CellPath(new_place, self)

    def generate_branchs(self, nodes: list[Cell]) -> list["CellPath"]:
        """Return one extended path for each cell in ``nodes``."""
        result: list[CellPath] = []
        for node in nodes:
            result.append(self.branch(node))
        return result

    def get_head(self) -> Cell:
        """Return the last cell of the path."""
        return self._head

    def get_head_direction(self) -> int:
        """Return the direction flag of the move that reached the head.

        Return 0 for the first cell of the path, which has no previous
        cell.
        """
        if self._rest is None:
            return 0
        return self._rest.get_head().get_cell_direction(self._head)

    def __str__(self) -> str:
        """Return the path as a string of ``N``, ``E``, ``S`` and ``W`` moves.

        The moves are listed from the entry to the exit.
        """
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
    """Generate, solve and save a rectangular maze.

    The maze is a ``width`` by ``height`` grid of ``Cell`` objects
    with the entry and the exit marked. ``execute`` runs the whole
    process.
    """
    _width: int = -1
    _height: int = -1
    _entry: tuple[int, int] = (0, 0)
    _exit: tuple[int, int] = (0, 0)
    _output_file: str = ""
    _perfect: bool = False
    _seed: int | None = None
    _maze_random: random.Random = random.Random()
    _grid: list[list[Cell]] = []
    _answer: CellPath | None = None

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
        """Store the maze settings, build the grid and mark the 42 pattern.

        If the maze is too small for the pattern, or the pattern covers
        the entry or the exit, the error is printed and the maze is
        built without it.

        Parameters
        ----------
        width : int
            Number of cells per row.
        height : int
            Number of rows.
        entry : tuple[int, int]
            ``(col, row)`` of the entry cell.
        exit : tuple[int, int]
            ``(col, row)`` of the exit cell.
        output : str
            Name of the file the maze is saved to.
        perfect : bool
            If True, the maze keeps a single path between any two cells.
        seed : int or None
            Seed of the maze random generator. If ``None``, the generator
            is not seeded.
        """
        self._width: int = width
        self._height: int = height
        self._entry: tuple[int, int] = entry
        self._exit: tuple[int, int] = exit
        self._output_file: str = output
        self._perfect: bool = perfect
        _answer: CellPath | None = None

        if seed is not None:
            self._seed = seed
            self._maze_random: random.Random = random.Random(seed)
        else:
            self._maze_random: random.Random = random.Random()

        self.create_grid()
        try:
            self.draw42()
        except Exception as error:
            print(f"Got Exception: {error}")

    def create_grid(self) -> None:
        """Build the grid with ``height`` rows of ``width`` closed cells.

        Any previous grid is discarded. The entry and exit cells are
        flagged.
        """
        self._grid: list[list[Cell]] = []
        for i in range(self._height):
            row: list[Cell] = []
            for j in range(self._width):
                cell: Cell = Cell(j, i)
                if (j, i) == self._entry:
                    cell._entry = True
                elif (j, i) == self._exit:
                    cell._exit = True
                row.append(cell)
            self._grid.append(row)

    def draw42(self) -> None:
        """Flag the cells that form the 42 pattern, centred in the maze.

        The pattern is 7 cells wide and 5 cells high, see ``FORTY_TWO``.

        Raises
        ------
        MazeConfigError
            If the maze is smaller than 9 by 7 cells, or if the pattern
            covers the entry or the exit.
        """
        if self._width < 9 or self._height < 7:
            raise MazeConfigError("The 42 pattern isn't possible to draw, the dimensions are too small")

        yy: int = (self._height // 2) - 2
        xx: int = (self._width // 2) - 3

        for point in FORTY_TWO:
            cell: Cell = self.get_cell((point[0] + xx, point[1] + yy))
            if cell.is_entry() or cell.is_exit():
                raise MazeConfigError("The 42 pattern collides with the exit and entry.")
            cell.set_forty_two(True)

    def not_perfect(self) -> None:
        """Open extra walls to remove the dead ends, creating loops.

        For each cell with three walls, except those of the 42 pattern,
        remove the wall towards a random neighbour. The maze then has
        more than one solution.
        """
        for line in self._grid:
            for block in line:
                if block.number_of_walls() == 3:
                    if block.is_forty_two():
                        continue

                    possibles: list[Cell] = self.get_not_possible_cells(block)
                    if len(possibles) != 0:
                        possible: Cell = self._maze_random.choice(possibles)
                        self.remove_wall(block, possible)

    def is_ouside(self, pos: tuple[int, int]) -> bool:
        """Return True if ``pos``, as ``(col, row)``, is outside the grid."""
        if pos[0] < 0 or pos[1] < 0:
            return True
        if pos[1] >= self._height or pos[0] >= self._width:
            return True
        return False

    def get_cell(self, pos: tuple[int, int]) -> Cell:
        """Return the cell at ``pos``, given as ``(col, row)``."""
        return self._grid[pos[1]][pos[0]]

    def random_cell(self) -> Cell:
        """Return a random cell of the grid."""
        return self.get_cell((self._maze_random.randint(0, self._width - 1),
                              self._maze_random.randint(0, self._height - 1)))

    def get_adjacent_cells(self, cell: Cell) -> list[Cell]:
        """Return the neighbours of ``cell`` that are inside the grid."""
        adjacent_pos: list[tuple[int, int]] = cell.get_adjacent_positions()
        return [self.get_cell(pos) for pos in adjacent_pos if
                not self.is_ouside(pos)]

    def get_possible_cells(self, cell: Cell) -> list[Cell]:
        """Return the neighbours of ``cell`` that have no wall in between."""
        return [c for c in self.get_adjacent_cells(cell) if
                not cell.check_wall(c)]

    def get_not_possible_cells(self, cell: Cell) -> list[Cell]:
        """Return the neighbours of ``cell`` that have a wall in between."""
        return [c for c in self.get_adjacent_cells(cell) if
                cell.check_wall(c) and not c.is_forty_two()]

    def remove_wall(self, cel1: Cell, cel2: Cell) -> None:
        """Remove the wall between two adjacent cells, on both sides."""
        cel1.remove_wall(cel2)
        cel2.remove_wall(cel1)

    def generate_maze(self) -> None:
        """Carve the maze with a randomised version of Prim's algorithm.

        Start with a random cell and keep a frontier of its unvisited
        neighbours. Each step takes a random cell of the frontier and
        joins it to a random visited neighbour, by removing the wall
        between them. The cells of the 42 pattern are never carved and
        never joined to their neighbours.
        """
        queue: list[Cell] = []
        stepped: set[Cell] = set()
        cell = self.random_cell()
        while cell._is_42:
            cell = self.random_cell()
        queue.append(cell)

        while len(queue) > 0:
            chosen: Cell = self._maze_random.choice(queue)
            queue.remove(chosen)

            if chosen.is_forty_two():
                stepped.add(chosen)
                continue

            if len(stepped) > 0:
                wall: Cell = self._maze_random.choice([
                    cell for cell in self.get_adjacent_cells(chosen) if
                    cell in stepped and not cell.is_forty_two()])
                self.remove_wall(chosen, wall)

            stepped.add(chosen)

            for i in self.get_adjacent_cells(chosen):
                if i not in stepped and i not in queue:
                    queue.append(i)

    def get_grid(self) -> list[list[Cell]]:
        """Return the cell grid, as a list of rows."""
        return self._grid

    def get_solution(self) -> CellPath:
        """Return the solution found by ``solve_maze``, or None before it."""
        return self._answer

    def insure_middle_42_free(self) -> None:
        """Open a corridor between the 4 and the 2 of the pattern.

        Remove the walls between the vertically consecutive cells of the
        middle column of the pattern, over its five rows. Each wall is
        removed on both sides.
        """
        yy: int = (self._height // 2) - 1
        xx: int = (self._width // 2)

        for hei in range(4):
            cell_x: Cell = self.get_cell((xx, yy + hei - 1))
            cell_y: Cell = self.get_cell((xx, yy + hei))
            self.remove_wall(cell_x, cell_y)

    def solve_maze(self) -> None:
        """Find the shortest path from the entry to the exit.

        Use a breadth-first search through the open passages. The path is
        stored in ``_answer``, as a ``CellPath`` that ends at the exit. If
        the exit cannot be reached, ``_answer`` is left unchanged.
        """
        queue: list[CellPath] = []
        stepped: set[Cell] = set()
        queue.append(CellPath(self.get_cell(self._entry)))

        while len(queue) > 0:
            chosen: CellPath = queue[0]
            chosen_head: Cell = chosen.get_head()

            queue.remove(chosen)
            stepped.add(chosen.get_head())

            for i in self.get_possible_cells(chosen_head):
                if i._exit:
                    self._answer = chosen.branch(i)
                    return
                if i not in stepped:
                    queue.append(chosen.branch(i))
                    stepped.add(i)

    def save_as_file(self) -> None:
        """Write the maze to ``_output_file``.

        The file holds one hexadecimal digit per cell, one grid row per
        line, then an empty line, the entry, the exit and the solution
        as a string of moves.
        """
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
        """Generate, solve and save the maze.

        If the maze is not perfect, its dead ends are opened after the
        generation and before the solving.
        """
        self.generate_maze()
        self.insure_middle_42_free()

        if not self._perfect:
            self.not_perfect()

        self.solve_maze()
        self.save_as_file()

    def show(self) -> None:
        """Print the maze settings to stdout."""
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
