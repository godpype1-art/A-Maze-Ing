import sys
import subprocess
from mazegen import Parser, ParserError, MazeGenerator, Display


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
                parser.verify_atributes()
            else:
                parser.show()
                raise ParserError(
                    "The following configurations "
                    f"are missing: {parser._missing}"
                    )
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
        try:
            maze_gen = MazeGenerator(
                parser._width,
                parser._height,
                parser._entry,
                parser._exit,
                parser._output_file,
                parser._perfect,
                parser._seed
            )
            maze_gen.execute()
            display = Display(
                maze_gen.get_grid(),
                parser._width,
                parser._height,
                maze_gen.get_solution()
                )
            display.cell_path()
            display.draw_maze()
        except Exception as error:
            print(f"Got Exception: {error}")
            sys.exit(1)
        else:
            while True:
                try:
                    display.display_menu()
                    option: str = input("Select option:").strip()
                    if option == "1":
                        subprocess.run("clear")
                        del display, maze_gen
                        maze_gen = MazeGenerator(
                            parser._width,
                            parser._height,
                            parser._entry,
                            parser._exit,
                            parser._output_file,
                            parser._perfect,
                            parser._seed
                        )
                        maze_gen.execute()
                        display = Display(
                            maze_gen.get_grid(),
                            parser._width,
                            parser._height,
                            maze_gen.get_solution()
                            )
                        display.cell_path()
                        display.draw_maze()
                    elif option == "2":
                        if display.show_path:
                            display.show_path = False
                        else:
                            display.show_path = True
                        subprocess.run("clear")
                        display.draw_maze()
                    elif option == "3":
                        display.alter_color()
                        subprocess.run("clear")
                        display.draw_maze()
                    elif option == "4":
                        sys.exit()
                    else:
                        subprocess.run("clear")
                        display.draw_maze()
                        print("Only 4 options man...")
                except (Exception, KeyboardInterrupt) as error:
                    print(f"Exception found: {error}")


if __name__ == "__main__":
    main()
