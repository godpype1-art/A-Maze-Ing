# runs the project
run:
	uv run python a_maze_ing.py config.txt


# intall the requirements
install:
	uv sync


# run in debug mode with python builtin debugger
debug:
	uv run python -m pdb a_maze_ing.py config.txt


# removes temporary files (pychache etc)
clean:
	rm -rf ...


# runs mypy and flake8
lint:
	uv run flake8 . && uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# runs mypy and flake8 --strict versions
lint-strict: #(optional)
	uv run flake8 . && uv run mypy . --strict

# builds the package
build:
	uv build


.PHONY: run install debug clean lint lint-strict build