#!/bin/bash

# -----
# Black
# -----
black --check . --diff

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
flake8 --ignore E203,E501,W503 . --statistics

# ----
# mypi
# ----
# https://github.com/python/mypy

