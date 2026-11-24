from .maze_generator import Cell, MazeGenerator
from .exceptions import MazeConfigError
from enum import Enum
from typing import Any
import subprocess
import sys


MAZE_BLOCK: str = "  "


OPTIONS: dict[int, str] = {
    1: "Regenerate maze",
    2: "Show/Hide solution",
    3: "Alternate maze colors",
    4: "Exit program"
}


class Color(list[str], Enum):
    ENTRY = ["42", "", ""]  # Green
    EXIT = ["41", "", ""]  # Red
    WALL = ["47", "", ""]  # White
    OPEN = ["40", "", ""]  # Black
    PATH = ["46", "", ""]  # Cyan
    FIXCELL = ["44", "", ""]  # Blue


class Display:

    # answer is the CellPath object with the solution to highlight
    def __init__(
            self, maze_grid: list[list[Cell]],
            maze_width: int, maze_height: int, answer: Any
            ) -> None:

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
        self.answer: Any = answer

        # The string to print the output with
        self.line: str | None = None

    # Calculates the color scheme to print
    def block_color(self, color: list[str]) -> str:
        return (f"\033[{color[self.color]}m{MAZE_BLOCK}\033[0m")

    # Converts the display index to maze_grid index
    def display_to_maze(self, index: int) -> int:
        return int((index - 1) / 2)

    # Converts the maze_grid index to display index
    def maze_to_display(self, index: int) -> int:
        return int(index * 2 + 1)

    # Draws wall line
    def draw_wall(self, i: int) -> str | None:

        for j in range(0, self.width):
            # Verify 1st or last line, first or last line block
            if i == 0 or i == self.height - 1 or j == 0 or j == self.width - 1:
                if self.line:
                    self.line += self.block_color(Color.WALL)
                else:
                    self.line = self.block_color(Color.WALL)
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
                # Verificar the cell_x ou cell_y tem 42flag OU sem cell_x
                # tem parede a norte e cell_y tem parede a sul
                if (
                    cell_x.fix_cell or cell_y.fix_cell or
                    (cell_x.walls >> 0 & 1 and cell_y.walls >> 2 & 1)
                        ):
                    self.line += self.block_color(Color.WALL)
                # Verify incoherence
                elif (
                    (cell_x.walls >> 0 & cell_y.walls >> 2) and
                    not (cell_x.walls >> 0 | cell_y.walls >> 2)
                        ):
                    raise MazeConfigError("Cell wall incoherence detected")
                # Open path
                else:
                    self.line += self.block_color(Color.OPEN)
        return self.line

    # Draws cell line
    def draw_path(self, i: int) -> str | None:

        for j in range(0, self.width):
            # Verify 1st or last line block
            if j == 0 or j == self.width - 1:
                if self.line:
                    self.line += self.block_color(Color.WALL)
                else:
                    self.line = self.block_color(Color.WALL)
            # Verify cell block itself
            elif j % 2 != 0:
                row: int = self.display_to_maze(i)
                col: int = self.display_to_maze(j)
                cell: Cell = self.grid[int(row)][int(col)]
                # Verify if cell is the entry point
                if cell.entry:
                    self.line += self.block_color(Color.ENTRY)
                # Verify if cell is the exit point
                elif cell.exit:
                    self.line += self.block_color(Color.EXIT)
                # Verify if cell is part of 42 logo
                elif cell.fix_cell:
                    self.line += self.block_color(Color.FIXCELL)
                elif self.show_path and cell._location in self.answer:
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
                # Verificar the cell_x ou cell_y tem 42flag OU
                # sem cell_x tem parede a este e cell_y tem parede a oeste
                if (
                    cell_x.fix_cell or cell_y.fix_cell or
                    (cell_x.walls >> 1 & 1 and cell_y.walls >> 3 & 1)
                        ):
                    self.line += self.block_color(Color.WALL)
                # Verify incoherence
                elif (
                    (cell_x.walls >> 1 & cell_y.walls >> 3) and
                    not (cell_x.walls >> 1 | cell_y.walls >> 3)
                        ):
                    raise MazeConfigError("Cell wall incoherence detected")
                # Else, the path is open
                else:
                    self.line += self.block_color(Color.OPEN)
        return self.line

    # Displays the maze
    def draw_maze(self) -> None:

        for i in range(0, self.height):
            self.line = None
            # Add here clock function to recreate animation for the bonus
            if i % 2 == 0:
                print(f"{self.draw_wall(i)}")
            elif i % 2 != 0:
                print(f"{self.draw_path(i)}")

    def alter_color(self):

        self.color += 1
        if self.color == 3:
            self.color = 0

    def display_menu(self) -> None:

        print()
        for key, value in OPTIONS.items():
            print(f"{key}. {value}")

    def display_loop(self) -> None:

        self.draw_maze()
        while True:
            try:
                self.display_menu()
                option: str = input("Select option:").strip()
                if option == "1":
                    subprocess.run("clear")
                    self.draw_maze()
                elif option == "2":
                    self.show_path = True
                    subprocess.run("clear")
                    self.draw_maze()
                elif option == "3":
                    self.alter_color()
                    subprocess.run("clear")
                    self.draw_maze()
                elif option == "4":
                    sys.exit()
                else:
                    subprocess.run("clear")
                    self.draw_maze()
                    print("Only 4 options man...")
            except (Exception, KeyboardInterrupt) as error:
                print(f"Exception found: {error}")


def main() -> None:
    try:
        maze: MazeGenerator = MazeGenerator(
            10, 10, (3, 3), (9, 9), "", False, None
            )
        maze.create_grid()
        maze.alter_maze()
        display: Display = Display(maze.grid, maze._width, maze._height, None)
        display.display_loop()

    except Exception as error:
        print(f"Exception found: {error}")


if __name__ == "__main__":
    main()
