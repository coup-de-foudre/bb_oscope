#!/bin/bash

python3 -m pytest oscope/*_tests.py --cov=oscope --cov-report=term-missing
