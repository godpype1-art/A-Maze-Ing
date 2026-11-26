from .maze_generator import Cell, CellPath
from .exceptions import MazeConfigError
from enum import Enum
from typing import Any


MAZE_BLOCK: str = "  "


OPTIONS: dict[int, str] = {
    1: "Re-generate maze",
    2: "Show/Hide solution",
    3: "Alternate maze colors",
    4: "Exit program"
}


class Color(list[str], Enum):
    """ANSI background codes for each cell type, one per palette.

    Every member holds three codes, selected with ``Display.color``:
    the basic 8-color code, a 256-color palette and an alternative
    256-color palette. A code goes between ``ESC[`` and ``m``.
    """
    ENTRY   = ["42", "48;5;46", "48;5;46"]    # Green
    EXIT    = ["41", "48;5;196", "48;5;196"]   # Red
    WALL    = ["47", "48;5;61", "48;5;240"]   # White / Slate Blue / Dark Grey
    OPEN    = ["40", "48;5;234", "48;5;255"]   # Black / Near Black / Near White
    PATH    = ["46", "48;5;220", "48;5;214"]   # Cyan / Gold / Orange
    FIXCELL = ["44", "48;5;133", "48;5;93"]    # Blue / Orchid / Purple


class Display:
    """Draw a maze in the terminal and run an interactive menu.

    The maze is drawn on a block grid of ``2 * width + 1`` columns by
    ``2 * height + 1`` rows. Odd positions hold the cells and even
    positions hold the walls between them, plus the outer border.
    """

    def __init__(
            self, maze_grid: list[list[Cell]],
            maze_width: int, maze_height: int, answer: Any
            ) -> None:
        """Store the maze data needed to draw it.

        Parameters
        ----------
        maze_grid : list[list[Cell]]
            Cell grid of the ``MazeGenerator``.
        maze_width : int
            Maze width, in cells.
        maze_height : int
            Maze height, in cells.
        answer : CellPath or None
            Solution to highlight, or ``None`` when there is none.
        """

        # Color palete from the Color Enum
        self.color: int = 0

        # The Cell grid from the MazeGenerator class
        self.grid: list[list[Cell]] = maze_grid

        # The display width built from the maze_width
        self.width: int = 2 * maze_width + 1

        # The display heigth built from the maze_height
        self.height: int = 2 * maze_height + 1

        # The boolean to show/hide the solution path
        self.show_path: bool = False

        # The solution to the maze (as the CellPath class)
        self.answer: CellPath = answer

        # The solution path
        self.path: list[tuple[int, int]] = []

        # The string to print the output with
        self.line: str = ""

    # Calculates the solution coordinates
    def cell_path(self) -> None:
        """Fill ``self.path`` with the locations of the solution cells.

        The ``answer`` chain is walked from the exit back to the entry,
        so it is consumed: ``self.answer`` ends up as ``None``.
        """
        while self.answer:
            self.path.append(self.answer._head._location)
            self.answer = self.answer._rest

    def block_color(self, color: list[str]) -> str:
        """Return one maze block painted with the active palette.

        Parameters
        ----------
        color : list[str]
            A ``Color`` member, indexed with ``self.color``.

        Returns
        -------
        str
            ``MAZE_BLOCK`` wrapped between the ANSI background code and
            the reset code.
        """
        return (f"\033[{color[self.color]}m{MAZE_BLOCK}\033[0m")

    def display_to_maze(self, index: int) -> int:
        """Convert a display index into a maze grid index.

        It is meant for the odd indices, which are the cell positions.
        """
        return int((index - 1) / 2)

    def maze_to_display(self, index: int) -> int:
        """Convert a maze grid index into a display index.

        The result is the odd index where the cell is drawn.
        """
        return int(index * 2 + 1)

    def draw_wall(self, i: int) -> str:
        """Build the display row ``i`` made of borders and horizontal walls.

        It is used for the even rows. The blocks are appended to
        ``self.line``, which is then returned. A block is a wall, an open
        passage, or part of the solution path when it is shown.

        Parameters
        ----------
        i : int
            Display row index (even).

        Returns
        -------
        str
            The painted row, ready to print.

        Raises
        ------
        MazeConfigError
            If two neighbouring cells disagree about the wall between
            them.
        """
        for j in range(0, self.width):
            # Verify 1st or last line, first or last line block
            if i == 0 or i == self.height - 1 or j == 0 or j == self.width - 1:
                self.line += self.block_color(Color.WALL)
            # Vereify corners
            elif j % 2 == 0:
                self.line += self.block_color(Color.WALL)
            # Verify wall
            else:
                col: int = self.display_to_maze(j)
                ix: int = self.display_to_maze(i - 1)
                iy: int = self.display_to_maze(i + 1)
                cell_x: Cell = self.grid[ix][col]
                cell_y: Cell = self.grid[iy][col]
                # Verify if the cell_x or cell_y have 42flag or if cell_x
                # has south wall and cell_y north wall
                if (
                    cell_x._is_42 or cell_y._is_42 or
                    (cell_x._walls >> 2 & 1 and cell_y._walls >> 0 & 1)
                        ):
                    self.line += self.block_color(Color.WALL)
                # Verify incoherence
                elif (
                    (cell_x._walls >> 2 & cell_y._walls >> 0) and
                    not (cell_x._walls >> 2 | cell_y._walls >> 0)
                        ):
                    raise MazeConfigError("Cell wall incoherence detected")
                # Open path
                else:
                    if (cell_x._location in self.path and cell_y._location in self.path) and self.show_path:
                        self.line += self.block_color(Color.PATH)
                    else:
                        self.line += self.block_color(Color.OPEN)
        return self.line

    def draw_path(self, i: int) -> str:
        """Build the display row ``i`` made of cells and vertical walls.

        It is used for the odd rows. Each cell is painted by its role
        (entry, exit, 42 logo, solution path or open), and between two
        cells there is a wall or an open passage. The blocks are appended
        to ``self.line``, which is then returned.

        Parameters
        ----------
        i : int
            Display row index (odd).

        Returns
        -------
        str
            The painted row, ready to print.

        Raises
        ------
        MazeConfigError
            If two neighbouring cells disagree about the wall between
            them.
        """
        for j in range(0, self.width):
            # Verify 1st or last line block
            if j == 0 or j == self.width - 1:
                self.line += self.block_color(Color.WALL)
            # Verify cell block itself
            elif j % 2 != 0:
                row: int = self.display_to_maze(i)
                col: int = self.display_to_maze(j)
                cell: Cell = self.grid[row][col]
                # Verify if cell is the entry point
                if cell._entry:
                    self.line += self.block_color(Color.ENTRY)
                # Verify if cell is the exit point
                elif cell._exit:
                    self.line += self.block_color(Color.EXIT)
                # Verify if cell is part of 42 logo
                elif cell._is_42:
                    self.line += self.block_color(Color.FIXCELL)
                elif self.show_path and cell._location in self.path:
                    self.line += self.block_color(Color.PATH)
                # Else, the path is open
                else:
                    self.line += self.block_color(Color.OPEN)
            # Verify wall
            elif j % 2 == 0:
                row: int = self.display_to_maze(i)
                jx: int = self.display_to_maze(j - 1)
                jy: int = self.display_to_maze(j + 1)
                cell_x: Cell = self.grid[row][jx]
                cell_y: Cell = self.grid[row][jy]
                # Verify if the cell_x or cell_y have 42flag or
                # if cell_x has east wall e cell_y has west wall
                if (
                    cell_x._is_42 or cell_y._is_42 or
                    (cell_x._walls >> 1 & 1 and cell_y._walls >> 3 & 1)
                        ):
                    self.line += self.block_color(Color.WALL)
                # Verify incoherence
                elif (
                    (cell_x._walls >> 1 & cell_y._walls >> 3) and
                    not (cell_x._walls >> 1 | cell_y._walls >> 3)
                        ):
                    raise MazeConfigError("Cell wall incoherence detected")
                # Else, the path is open
                else:
                    if (cell_x._location in self.path and cell_y._location in self.path) and self.show_path:
                        self.line += self.block_color(Color.PATH)
                    else:
                        self.line += self.block_color(Color.OPEN)
        return self.line

    def draw_maze(self) -> None:
        """Print the whole maze, one display row at a time."""

        for i in range(0, self.height):
            self.line = ""
            if i % 2 == 0:
                print(f"{self.draw_wall(i)}")
            elif i % 2 != 0:
                print(f"{self.draw_path(i)}")

    def alter_color(self):
        """Switch to the next color palette.

        After the last palette it goes back to the first one.
        """

        self.color += 1
        if self.color == 3:
            self.color = 0

    def display_menu(self) -> None:
        """Print the numbered menu options."""

        print("=== A-maze-ing ===")
        for key, value in OPTIONS.items():
            print(f"{key}. {value}")

