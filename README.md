*This project has been created as part of the 42 curriculum by falves-e, afranco-.*

# A-Maze-ing

A maze generator written in Python. It reads a configuration file, generates a
maze (perfect or playable), writes it to a file using a hexadecimal wall
encoding, and displays it in the terminal with an interactive menu. The
generation logic is packaged as a reusable library called `mazegen`.

## Description

**Goal.** Build a maze generator that is random but reproducible (seed), valid
(coherent walls, full connectivity, closed borders), and reusable in a later
project.

**Overview.**

- Reads a `KEY=VALUE` configuration file and validates it, reporting clear
  errors instead of crashing.
- Generates a maze in one of two modes:
  - `PERFECT=True`: exactly one path between any two cells (no loops).
  - `PERFECT=False` (default): a playable, Pac-Man-like board with loops and
    very few dead-ends.
- Draws a visible **"42"** made of fully closed cells in the centre of the
  maze. If the maze is too small, the pattern is omitted and an error message
  is printed.
- Computes the shortest path from the entry to the exit (breadth-first search).
- Writes the maze, the entry, the exit and the shortest path to an output file.
- Displays the maze in the terminal (ANSI colours) with a menu to regenerate
  it, show or hide the solution and change the colours.
- Ships the generator as an installable package (`mazegen-*.whl` / `.tar.gz`).

### Project structure

| Path | Role |
| --- | --- |
| `a_maze_ing.py` | Main program: error handling and the interactive menu loop |
| `mazegen/parser.py` | `Parser`: reads and validates the configuration file |
| `mazegen/maze_generator.py` | `MazeGenerator`, `Cell`, `CellPath`: generation, solving, output file |
| `mazegen/display.py` | `Display`: terminal rendering, colour palettes, menu options |
| `mazegen/exceptions.py` | `ParserError`, `MazeConfigError`, `MazeInternalError` |
| `config.txt` | Default configuration file |
| `Makefile` | `install`, `run`, `debug`, `clean`, `lint`, `lint-strict`, `build` |
| `pyproject.toml` | Package metadata and build configuration |
| `LICENSE.md` | MIT license |

## Instructions

### Requirements

- Python 3.10 or later
- [uv](https://docs.astral.sh/uv/) (used to install the dependencies and to
  build the package)
- A terminal with 256-colour support

### Installation

```bash
git clone <repository-url>
cd A-Maze-ing
make install        # uv sync
```

### Execution

```bash
make run            # uv run python a_maze_ing.py config.txt
# or
python3 a_maze_ing.py config.txt
```

The configuration file is the only argument. When the maze is displayed, a menu
is shown:

| Option | Action |
| --- | --- |
| `1` | Re-generate a new maze and display it (uses the same configuration, so a configuration with a `SEED` always gives the same maze) |
| `2` | Show / hide the shortest path from the entry to the exit |
| `3` | Change the colours (cycles through 3 palettes) |
| `4` | Exit the program |

### Makefile rules

| Rule | Description |
| --- | --- |
| `make install` | Install the dependencies (`uv sync`) |
| `make run` | Run `a_maze_ing.py` with `config.txt` |
| `make debug` | Run the program with Python's debugger (`pdb`) |
| `make clean` | Remove caches and build leftovers (`__pycache__`, `.mypy_cache`, ...) |
| `make fclean` | `clean` + remove the built package and the virtual environment |
| `make lint` | `flake8` and `mypy` with the flags required by the subject |
| `make lint-strict` | `flake8` and `mypy --strict` |
| `make build` | Build the package (`mazegen-*.whl` and `.tar.gz`) in the repository root |

## Configuration file

The file contains one `KEY=VALUE` pair per line. Lines starting with `#` are
comments and are ignored. Keys are case-sensitive.

| Key | Required | Description | Example |
| --- | --- | --- | --- |
| `WIDTH` | yes | Maze width, in cells | `WIDTH=20` |
| `HEIGHT` | yes | Maze height, in cells | `HEIGHT=15` |
| `ENTRY` | yes | Entry coordinates `x,y` (origin at the top-left cell) | `ENTRY=0,0` |
| `EXIT` | yes | Exit coordinates `x,y` | `EXIT=19,14` |
| `OUTPUT_FILE` | yes | Name of the output file | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | yes | `True`: perfect maze. `False`: playable board with loops (case-insensitive) | `PERFECT=True` |
| `SEED` | no | Seed of the random generator. The same configuration and seed always give the same maze | `SEED=42` |

Example (`config.txt`):

```
# Maze size, in number of cells
WIDTH=20
HEIGHT=15
# Coordinates are x,y
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42
```

Rules checked by the parser:

- Duplicated keys and unknown keys are reported and discarded.
- A line that is not a `KEY=VALUE` pair, or has an empty key or value, is
  reported and discarded.
- `PERFECT` must be `True` or `False`.
- Missing mandatory keys are listed in the error message.
- The entry and the exit must be different and inside the maze.

Every error is printed as a clear message and the program exits instead of
crashing.

## Output file format

The output file has one hexadecimal digit per cell, one row per line. Each digit
encodes the **closed** walls of the cell (bit set to 1 = wall):

| Bit | Direction |
| --- | --- |
| 0 (LSB) | North (value 1) |
| 1 | East (value 2) |
| 2 | South (value 4) |
| 3 | West (value 8) |

After the grid there is an empty line, then three lines: the entry coordinates,
the exit coordinates and the shortest path from the entry to the exit using the
letters `N`, `E`, `S`, `W`. All lines end with `\n`.

Example (9x7 maze, `ENTRY=0,0`, `EXIT=8,6`, `PERFECT=True`, `SEED=7`). The `f`
digits are the fully closed cells of the "42" pattern:

```
951795553
af812fffa
afec057fa
afffafffa
a93fafd56
aaafafffb
c6c545556

0,0
8,6
EESEESSSSSEEEE
```

Neighbouring cells always agree on their shared wall, and the outer border is
closed.

## Maze generation algorithm

**Algorithm: randomised Prim's algorithm**, followed by a breadth-first search
to solve the maze.

1. Pick a random starting cell (never a cell of the "42" pattern) and put it in
   the *frontier*.
2. Repeat until the frontier is empty: take a random cell from the frontier,
   open the wall between it and a random neighbour that is already part of the
   maze, then add its not-yet-visited neighbours to the frontier.
3. Cells of the "42" pattern are never carved, so they stay fully closed. A
   corridor is then opened in the column between the "4" and the "2" so the
   pattern does not split the board.
4. If `PERFECT=False`, every dead-end (cell with three walls, outside the "42"
   pattern) gets one extra wall removed towards a random neighbour. This creates
   loops (a "braided" maze) and leaves very few dead-ends.
5. A breadth-first search from the entry finds the shortest path to the exit.

All random choices use a `random.Random` instance created from `SEED`, which
makes the maze reproducible.

**The "42" pattern** is 7 cells wide and 5 cells high and is centred in the maze.
The minimum maze size is 9x7. For smaller mazes the pattern is omitted and an
error message is printed.

**Why this algorithm.**

- Every cell is joined to the maze exactly once, so the result is a spanning
  tree: a perfect maze by construction (one path between any two cells, full
  connectivity, no isolated cell).
- It is easy to exclude the cells of the "42" pattern from the carving.
- It produces many short branches, which gives a maze that is hard to read at a
  glance, and it runs in time proportional to the number of cells.
- The perfect maze is a good base for the non-perfect mode: removing walls at
  the dead-ends adds loops without breaking connectivity.
- It works with a seeded random generator, so results are reproducible.

## Visual representation

The maze is displayed in the terminal. Each block is two spaces painted with an
ANSI background colour (two spaces look roughly square). The display is a grid
of `2 * WIDTH + 1` by `2 * HEIGHT + 1` blocks: odd positions are cells, even
positions are walls and the border.

- Entry in green, exit in red, the "42" pattern in its own colour, and the
  shortest path highlighted when it is shown.
- Three colour palettes (option `3`): the basic 8 colours, a 256-colour palette
  (slate walls, dark floor, gold path) and an alternative 256-colour palette
  (dark walls, light floor, orange path).

## Reusable code

The maze generation is a standalone class, `MazeGenerator`, in
`mazegen/maze_generator.py`. It only depends on the Python standard library and
on `mazegen.exceptions`, and does not need the parser or the display.

### Build and install the package

```bash
make build                                   # creates mazegen-1.0.0-py3-none-any.whl
pip install mazegen-1.0.0-py3-none-any.whl   # in your own project or virtualenv
```

The `.tar.gz` source archive is built alongside the wheel and can be installed
the same way. Everything needed to rebuild the package is in the repository
(`pyproject.toml`, the `mazegen/` folder and `LICENSE.md`).

### Basic example

```python
from mazegen import MazeGenerator
from mazegen.maze_generator import NORTH, EAST, SOUTH, WEST

maze = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    output="maze.txt",
    perfect=True,
    seed=42,
)
maze.execute()                    # generate, solve and write maze.txt

grid = maze.get_grid()            # list of rows, each row a list of Cell
cell = grid[0][0]                 # row 0, column 0
print(cell.get_location())        # (0, 0)
print(cell.get_hexadecimal())     # the hex digit written in the output file
print(bool(cell.get_walls() & NORTH))   # True if the north wall is closed

solution = maze.get_solution()    # CellPath: the shortest path
print(str(solution))              # moves from entry to exit, e.g. "SESS..."
print(solution.get_size())        # number of moves
```

### Custom parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `width`, `height` | `int` | Maze size in cells (the "42" pattern needs at least 9x7) |
| `entry`, `exit` | `tuple[int, int]` | `(x, y)` coordinates, origin at the top-left cell |
| `output` | `str` | File written by `execute()` / `save_as_file()` |
| `perfect` | `bool` | `True`: no loops. `False`: loops and very few dead-ends |
| `seed` | `int` or `None` | Same parameters and same seed give the same maze. `None` is not reproducible |

### Accessing the maze and the solution

- `maze.get_grid()` returns the maze as a list of rows of `Cell` objects, indexed
  `grid[y][x]`.
- A `Cell` stores its walls as a bitmask (`NORTH` = 1, `EAST` = 2, `SOUTH` = 4,
  `WEST` = 8, bit set = closed wall). Useful methods: `get_location()`,
  `get_walls()`, `check_walls(direction)`, `check_wall(neighbour)`,
  `number_of_walls()`, `get_hexadecimal()`, `is_entry()`, `is_exit()`,
  `is_forty_two()`.
- `maze.get_solution()` returns a `CellPath`, available after `solve_maze()` or
  `execute()`. `str(solution)` gives the moves (`N`, `E`, `S`, `W`) and
  `get_size()` gives their number.
- The steps can also be run one by one: `generate_maze()`, `solve_maze()` and
  `save_as_file()`. `execute()` runs the full sequence.

## Team and project management

**Roles**

- **falves-e**: terminal display and colour palettes, interactive menu, project
  structure, Makefile and documentation.
- **afranco-**: maze generator (generation, perfect and non-perfect modes, "42"
  pattern, solving).

**Planning and how it evolved**

The Git history shows the work starting with study and tests (10 Nov 2026), a
first display and the first generator (18 and 19 Nov), then the generator and
display working with the `PERFECT` flag, the non-perfect mode (24 Nov) and the
"42" pattern with the final fixes (26 Nov).

We did not plan much beyond deciding each person's role in the project. In
practice, whoever had free time at the moment worked on the project.

**What worked well and what could be improved**

The project went well: we built a working program fairly quickly.

The part that could have gone better was putting the pieces together. Our ways
of thinking about the problem were quite different, so joining our parts into
one coherent program turned out to be a bigger challenge than we expected.

**Tools used**

- Git and GitHub, with one branch per person and pull requests
- [uv](https://docs.astral.sh/uv/) for dependencies and the package build
- `make` for the common tasks
- `flake8` and `mypy` for linting and type checking
- Claude (AI assistant), see the Resources section

## Resources

**References**

- [Maze generation algorithm (Wikipedia)](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Prim's algorithm (Wikipedia)](https://en.wikipedia.org/wiki/Prim%27s_algorithm)
- [Maze Generation: Prim's Algorithm (Jamis Buck)](http://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm)
- [Breadth-first search (Wikipedia)](https://en.wikipedia.org/wiki/Breadth-first_search)
- [ANSI escape code (Wikipedia)](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [PEP 257: Docstring conventions](https://peps.python.org/pep-0257/)
- [Python `random` module](https://docs.python.org/3/library/random.html)
- [uv documentation](https://docs.astral.sh/uv/)

**How AI was used**

We used Claude (Anthropic) mostly like a search engine: to look things up and
to learn new concepts, for example how ANSI escape sequences colour the
terminal and how the 256-colour format works. It also helped with the less fun
parts of the project:

- writing the PEP 257 docstrings in the `mazegen` files
- writing this README and the license file

This project does not contain any code written by AI.

## License

This project is distributed under the MIT License, see [LICENSE.md](LICENSE.md).
The license explicitly allows the `mazegen` package to be reused, modified and
distributed by later projects.
