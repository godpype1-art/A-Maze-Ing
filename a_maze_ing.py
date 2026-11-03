import sys
from mazegen import Parser, ParserError, MazeGenerator


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
        maze_gen = MazeGenerator(
            parser._width,
            parser._height,
            parser._entry,
            parser._exit,
            parser._output_file,
            parser._perfect,
            parser._seed
        )
        maze_gen.show()
        print()
        maze_gen.create_grid()


if __name__ == "__main__":
    main()
