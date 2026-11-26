import sys
from .exceptions import ParserError, MazeConfigError


class Parser():
    """Read, convert and validate the maze settings from a config file.

    The methods are meant to be called in this order: ``parsing``,
    ``verify_missing``, ``set_data`` and ``verify_atributes``.
    ``show`` can be called at any point to print the current state.
    The settings are kept in the private attributes (``_width``,
    ``_entry``, ...).
    """

    _maze_config: dict[str, str] = {}
    """Raw key/value pairs read from the config file."""

    _missing: list[str] = []
    """Mandatory keys that are absent from the config file."""

    _width: int = -1
    """Maze width, in cells."""

    _height: int = -1
    """Maze height, in cells."""

    _entry: tuple[int, int]
    """Maze entry point, as an ``(x, y)`` tuple."""

    _exit: tuple[int, int]
    """Maze exit point, as an ``(x, y)`` tuple."""

    _output_file: str = ""
    """Name of the file the maze is saved to."""

    _perfect: bool = False
    """Whether the maze must have a single solution."""

    _seed: int | None = None
    """Seed for the maze generation, if the config gives one."""

    _parameters: list[str] = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
        "SEED"
    ]
    """Every key accepted in the config file."""

    def __init__(self) -> None:
        """Set every setting to its default value."""
        self._maze_config: dict[str, str] = {}
        self._missing: list[str] = []
        self._width: int = -1
        self._height: int = -1
        self._entry: tuple[int, int]
        self._exit: tuple[int, int]
        self._output_file: str = ""
        self._perfect: bool = False
        self._seed: int | None = None
        self._parameters: set[str] = [
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT",
            "SEED"
        ]

    def parsing(self, filename: str) -> None:
        """Read ``filename`` and store its ``KEY=VALUE`` pairs.

        Lines starting with ``#`` are skipped. Valid pairs are saved in
        ``self._maze_config`` and the ``PERFECT`` value is also converted
        to a bool in ``self._perfect``. A malformed line is reported on
        stdout and discarded instead of raising, and an unreadable file
        is reported the same way. Any unexpected error ends the program
        with exit status 1.

        Parameters
        ----------
        filename : str
            Path of the config file to read.
        """
        try:
            with open(filename, "r") as file:
                lines: list[str] = file.readlines()
        except (OSError, ValueError) as error:
            print(f"Got Exception: {error}")
        else:
            for i, line in enumerate(lines):
                if line.startswith("#"):
                    continue
                else:
                    try:
                        data: list[str] = line.split("=", 1)
                        data[0], data[1] = data[0].strip(), data[1].strip()
                        if len(data) != 2:
                            raise ParserError(
                                f"[LINE {i}] Key=Value pair "
                                "is in the wrong format"
                                )
                        if not data[0].strip() or not data[1].strip():
                            raise ParserError(
                                f"[LINE {i}] It must be in a Key=Value pair"
                                )
                        if data[0] in self._maze_config.keys():
                            raise ParserError(
                                f"[LINE {i}] Parameter duplicated - discarding"
                                )
                        if data[0] not in self._parameters:
                            raise ParserError(
                                f"[LINE {i}] Unknown KEY read - discarding"
                                )
                        if data[0] in "PERFECT":
                            data[1] = data[1].lower()
                            if data[1] in ["true", "false"]:
                                if data[1] == "true":
                                    self._perfect = True
                                else:
                                    self._perfect = False
                            else:
                                raise ParserError(
                                    f"[LINE {i}] Wrong config for "
                                    "'PERFECT' parameter"
                                    )
                        self._maze_config[data[0]] = data[1]
                    except ParserError as error:
                        print(error)
                    except Exception as error:
                        print(f"[LINE {i}] GOT UNEXPECTED EXCEPTION: {error}")
                        sys.exit(1)

    def set_data(self) -> None:
        """Convert the parsed strings into typed attributes.

        Fill ``_width``, ``_height``, ``_entry``, ``_exit``,
        ``_output_file`` and, when present, ``_seed`` from
        ``_maze_config``. The mandatory keys must be there, see
        ``verify_missing``.

        Raises
        ------
        KeyError
            If a mandatory key is missing from ``_maze_config``.
        ParserError
            If a coordinate of ``ENTRY`` or ``EXIT`` is empty.
        ValueError
            If a number, or an ``x,y`` pair, cannot be converted.
        """
        self._width = int(self._maze_config["WIDTH"])
        self._height = int(self._maze_config["HEIGHT"])
        x, y = self._maze_config["ENTRY"].split(",", 1)
        if not x or not y:
            raise ParserError("Wrong config for 'ENTRY'")
        self._entry = (int(x), int(y))
        x, y = self._maze_config["EXIT"].split(",", 1)
        if not x or not y:
            raise ParserError("Wrong config for 'EXIT'")
        self._exit = (int(x), int(y))
        self._output_file = self._maze_config["OUTPUT_FILE"]
        if "SEED" in self._maze_config.keys():
            self._seed = int(self._maze_config["SEED"])

    def verify_missing(self) -> None:
        """Record the mandatory config keys that are missing.

        The missing keys are appended to ``_missing``. ``SEED`` is
        optional, so it is never reported.
        """
        for param in self._parameters:
            if param == "SEED":
                continue
            if param not in self._maze_config.keys():
                self._missing.append(param)

    def verify_atributes(self) -> None:
        """Check that the entry and exit points are usable.

        Raises
        ------
        MazeConfigError
            If the entry and the exit are the same point, or if a
            coordinate goes beyond the maze width or height.
        """

        if self._entry == self._exit:
            raise MazeConfigError(
                "The entry and exit points can't be the same"
                )
        x1, y1 = self._entry
        x2, y2 = self._exit
        if x1 > self._width or x2 > self._width:
            raise MazeConfigError(
                "The entry and exit points need to be within maze boundaries"
                )
        if y1 > self._height or y2 > self._height:
            raise MazeConfigError(
                "The entry and exit points need to be within maze boundaries"
                )

    def show(self) -> None:
        """Print the parsed configuration to stdout."""
        print(
            "============= DATA ==============",
            f"Data parsed: {self._maze_config}",
            "",
            "Data colected:",
            f"  Width: {self._width}",
            f"  Height: {self._height}",
            f"  Entry: {self._entry}",
            f"  Exit: {self._exit}",
            f"  Output File: {self._output_file}",
            f"  Perfect: {self._perfect}",
            sep="\n"
            )
