@echo off
mkdir data
python scripts\seed_data.py
python run.py
pause
