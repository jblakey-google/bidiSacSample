# Makefile for running a simple shell command.

# By convention, 'all' is the default target.
# We'll make it depend on our 'hello' target.
all: run

# This target runs the echo command.
# The '@' symbol at the beginning of the line prevents 'make'
# from printing the command before it executes it, resulting in cleaner output.
hello:
	@echo "Hello, World!"

install:
	pip install -r requirements.txt

run:
	python sample.py

# It's good practice to declare targets that don't create files as .PHONY.
# This tells 'make' to always run the command for this target, even if a
# file named 'hello' happens to exist.
.PHONY: all hello
