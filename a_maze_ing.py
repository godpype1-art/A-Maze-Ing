import sys
import typing
from enum import Enum


class ParserError(Exception):
    ...


class Data(Enum):
    WIDTH = "width"
    HEIGHT = "height"
    ENTRY = "entry"
    EXIT = "exit"
    OUTPUT_FILE = "output file"
    PERFECT = "perfect"


class Parser():
    _file = ""
    _maze_config: dict[str, str] = {}
    _test: list[str] = []

    def __init__(self, filename: str) -> None:
        self._file = filename
        self.parsing(self._file)


    def parsing(self, filename: str) -> None:
        try:
            file: typing.IO = open(filename, "r")
            raw: str = file.read()
        except OSError as error:
            print(f"Got Exception: {error}")
            return
        else:
            lines: list[str] = raw.split('\n')
            for line in lines:
                if line.startswith("#"):
                    continue
                else:
                    self._test.append(line)
            print(self._test)


    def show(self) -> None:
        print(f"File to open: {self._file}")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python a_maze_ing.py config.txt")
        return
    try:
        if sys.argv[1].strip() != "config.txt":
            raise ParserError(f"Invalid config.txt: {sys.argv[1]}")
        else:
            filename: str = sys.argv[1].strip()
            parser = Parser(filename)
            parser.show()
    except ParserError as error:
        print(f"Got exception: {error}")
    else:
        return


if __name__ == "__main__":
    main()
