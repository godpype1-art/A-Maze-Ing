import sys
from typing import Any


class ParserError(Exception):
    ...


class Parser():
    def __init__(self) -> None:
        self._maze_config: Any = {}
        self._width: int = -1
        self._height: int = -1
        self._entry: tuple[int, int] = []
        self._exit: tuple[int, int] = []
        self._output_file: str = ""
        self._perfect: bool = False


    def parsing(self, filename: str) -> None:

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
                        if len(data) != 2:
                            raise ParserError(f"[LINE {i}] Key=Value pair is in the wrong format")
                        if not data[0].strip() or not data[1].strip():
                            raise ParserError(f"[LINE {i}] It must be in a Key=Value pair")
                        self._maze_config[data[0].strip()] = data[1].strip()
                    except ParserError as error:
                        print(error)
                    except Exception as error:
                        print(f"[LINE {i}]GOT UNEXPECTED EXCEPTION {error}")


    def show(self) -> None:
        print(
            "============= DATA ==============",
            f"Data parsed: {self._maze_config}",
            sep="\n"
            )


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python a_maze_ing.py config.txt")
        return
    try:
        if sys.argv[1].strip() != "config.txt":
            raise ParserError(f"Invalid config.txt: {sys.argv[1]}")
        else:
            filename: str = sys.argv[1].strip()
            parser = Parser()
            parser.parsing(filename)
            parser.show()
    except ParserError as error:
        print(f"Got exception: {error}")
    else:
        return


if __name__ == "__main__":
    main()
