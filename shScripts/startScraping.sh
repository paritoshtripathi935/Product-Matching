#!/bin/bash

# Change to the project directory
cd /home/pamripose/myprojects/Product-Matching

# Activate the virtual environment
source venv/bin/activate

# Run the Python script
python3 data/Amazon/scripts/main.py

bash push-amazon.sh