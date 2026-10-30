import sys


class ParserError(Exception):
    ...


class MazeConfigError(Exception):
    ...


class Parser():
    def __init__(self) -> None:
        self._maze_config: dict[str, str] = {}
        self._missing: list[str] = []
        self._width: int = -1
        self._height: int = -1
        self._entry: tuple[int, int] = []
        self._exit: tuple[int, int] = []
        self._output_file: str = ""
        self._perfect: bool = False
        self._seed: int = -1

        self._parameters: set = [
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT",
            "SEED"
        ]


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
                        data[0], data[1] = data[0].strip(), data[1].strip()
                        if len(data) != 2:
                            raise ParserError(f"[LINE {i}] Key=Value pair is in the wrong format")
                        if not data[0].strip() or not data[1].strip():
                            raise ParserError(f"[LINE {i}] It must be in a Key=Value pair")
                        if data[0] in self._maze_config.keys():
                            raise ParserError(f"[LINE {i}] Parameter duplicated - discarding")
                        if data[0] not in self._parameters:
                            raise ParserError(f"[LINE {i}] Unknown KEY read - discarding")
                        if data[0] in "PERFECT":
                            data[1] = data[1].lower()
                            if data[1] in ["true", "false"]:
                                if data[1] == "true":
                                    self._perfect = True
                                else:
                                    self._perfect = False
                            else:
                                raise ParserError(f"[LINE {i}] Wrong config for 'PERFECT' parameter")
                        self._maze_config[data[0]] = data[1]
                    except ParserError as error:
                        print(error)
                    except Exception as error:
                        print(f"[LINE {i}] GOT UNEXPECTED EXCEPTION: {error}")
                        sys.exit(1)


    def set_data(self) -> None:

        self._width = int(self._maze_config["WIDTH"])
        self._height = int(self._maze_config["HEIGHT"])
        x, y = self._maze_config["ENTRY"].split(",", 1)
        if not x or not y:
            raise ParserError("Wrong config for 'ENTRY'")
        self._entry = [int(x), int(y)]
        x, y = self._maze_config["EXIT"].split(",", 1)
        if not x or not y:
            raise ParserError("Wrong config for 'EXIT'")
        self._exit = [int(x), int(y)]
        self._output_file = self._maze_config["OUTPUT_FILE"]
        if "SEED" in self._maze_config.keys():
            self._seed = self._maze_config["SEED"]


    def verify_missing(self) -> None:
        for param in self._parameters:
            if param == "SEED":
                continue
            if param not in self._maze_config.keys():
                self._missing.append(param)


    def verify_atributes(self) -> None:

        if self._entry == self._exit:
            raise MazeConfigError("The entry and exit points can't be the same")
        x1, y1 = self._entry
        x2, y2 = self._exit
        if x1 > self._width or x2 > self._width:
            raise MazeConfigError("The entry and exit points need to be within maze boundaries")
        if y1 > self._height or y2 > self._height:
            raise MazeConfigError("The entry and exit points need to be within maze boundaries")



    def show(self) -> None:
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
            parser.verify_missing()
            if not parser._missing:
                parser.set_data()
                parser.show()
                parser.verify_atributes()
            else:
                parser.show()
                raise ParserError(f"The following configurations are missing: {parser._missing}")
    except ParserError as error:
        print(f"Got exception: {error}")
        sys.exit(1)
    except ValueError as error:
        print(f"Got exception: {error}")
        sys.exit(1)
    except Exception as error:
        print(f"GOT UNEXPECTED EXCEPTION: {error}")
        sys.exit(1) 
    else:
        return


if __name__ == "__main__":
    main()
