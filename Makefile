CONFIG ?= config.ini
MODE ?= all

.PHONY: run test

run:
	python3 -m src.main $(CONFIG) $(MODE)

test:
	python3 -m unittest -v
