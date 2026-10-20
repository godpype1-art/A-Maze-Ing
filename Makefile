# must contain following rules

srcs:
	a_maze_ing.py

helpers:
	requirements.txt
	config.txt



# intall the requirements
install:
	pip install -r requirements.txt


# runs the project
run:
	python3 a_maze_ing.py config.txt


# run in debug mode with python builtin debugger
debug:
	python3 -m pdb ...


# removes temporary files (pychache etc)
clean:
	rm -f ...
	rm -d ...


# runs mypy and flake8
lint:


# runs mypy and flake8 --strict versions
lint-strict: #(optional)


.PHONY: 