UV         := uv
FLAKE8     := $(UV) run flake8 --exclude=.venv,.git,build,dist .
MYPY       := $(UV) run mypy .


# runs the project
run:
	$(UV) run python a_maze_ing.py config.txt


# intall the requirements
install:
	$(UV) sync


# run in debug mode with python builtin debugger
debug:
	$(UV) run python -m pdb a_maze_ing.py config.txt


# removes temporary files (pychache etc)
clean:
	rm -rf __pycache__ mazegen/__pycache__ .mypy_cache mazegen/.mypy_cache .pytest_cache \
		build dist *.egg-info


# runs mypy and flake8
lint:
	$(FLAKE8)
	$(MYPY) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# runs mypy and flake8 --strict versions
lint-strict:
	$(FLAKE8)
	$(MYPY) --strict

# builds the package
build:
	$(UV) build --out-dir .


.PHONY: run install debug clean lint lint-strict build