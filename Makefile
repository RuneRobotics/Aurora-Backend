# Name of your conda environment
ENV_NAME = Aurora

.PHONY: run
run:
	@mkdir -p logs; \
	conda run -n $(ENV_NAME) python -u -X faulthandler code/src/main.py

.PHONY: install
install:
	conda env create -f environment.yml || conda env update -f environment.yml