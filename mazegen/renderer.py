from .maze_generator import Cell, MazeGenerator
from .exceptions import MazeConfigError
from enum import Enum
from typing import Any


MAZE_BLOCK: str = "  "


class Color(Enum, list[str]):
    ENTRY = ["42", "", ""]
    EXIT = ["41", "", ""]
    WALL = ["47", "", ""]
    OPEN = ["40", "", ""]
    PATH = ["46", "", ""]
    FIXCELL = ["44", "", ""]


class Display:

    # answer is the CellPath object with the solution to highlight
    def __init__(self, maze_grid: list[list[Cell]], maze_width: int, maze_height: int, answer: Any) -> None:

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
        return((index - 1) / 2)

    # Converts the maze_grid index to display index
    def maze_to_display(self, index: int) -> int:
        return(index * 2 + 1)
    
    # Draws wall line
    def draw_wall(self, i: int) -> str:

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
                # Verificar the cell_x ou cell_y tem 42flag OU sem cell_x tem parede a norte e cell_y tem parede a sul
                if cell_x.fixcell or cell_y.fixcell or (cell_x << 0 == 1 and cell_y << 2 == 1):
                    self.line += self.block_color(Color.WALL)
                # Verify incoherence
                elif cell_x << 0 != cell_y << 2:
                    raise MazeConfigError("Cell wall incoherence detected")
                # Open path
                else:
                    self.line += self.block_color(Color.OPEN)
        return self.line


    # Draws cell line
    def draw_path(self, i: int) -> str:

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
                # Verificar the cell_x ou cell_y tem 42flag OU sem cell_x tem parede a este e cell_y tem parede a oeste
                if cell_x.fixcell or cell_y.fixcell or (cell_x << 1 == 1 and cell_y << 3 == 1):
                    self.line += self.block_color(Color.WALL)
                # Verify incoherence
                elif cell_x << 1 != cell_y << 3:
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

    # Add method to handle path visualization
    #def path_highlight

    # Add text for input options methods
    #def input_options()

    # Add display method, which will call the visualization structure
    #def display()
        #self.draw_maze()
        #self.input_options()
        #??self.show_path??


def main() -> None:
    print("\033[44m  \033[0m\033[42m  \033[0m\033[47m  \033[0m")



if __name__ == "__main__":
    main()


