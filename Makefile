# Name of your conda environment
ENV_NAME = Aurora

# Default target
.PHONY: run
run:
	conda run -n $(ENV_NAME) python code/src/main.py

.PHONY: install
install:
	conda env create -f environment.yml || conda env update -f environment.yml