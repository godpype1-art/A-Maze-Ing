class Cell():
    _location = []
    _walls = []

    def __init__(self, x: int, y: int) -> None:
        self._location: tuple[int, int] = [x, y]
        self._walls: list[bool] = [True, True, True, True]


class MazeGenerator():
    _width: int = -1
    _height: int = -1
    _entry: tuple[int, int] = []
    _exit: tuple[int, int] = []
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
