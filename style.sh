#!/bin/bash

# -----
# Black
# -----
black --check . --diff
# black --check . --diff --line-length=79

# ------
# flake8
# ------
# flake8 errors:
# E501 line too long (## > 79 characters)
# E203 whitespace before ':'
#
# flake8 warnings:
# W503 line break occurred before a binary operator
#
# flake8 . --statistics
# E501 - line length exceeds 79 characters
# https://peps.python.org/pep-0008/#maximum-line-length
flake8 --ignore E203,E501,W503 . --statistics

# ----
# mypi
# ----
# https://github.com/python/mypy

