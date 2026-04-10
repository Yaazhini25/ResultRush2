#!/bin/bash
cd "$(dirname "$0")"
mkdir -p data
python scripts/seed_data.py
python run.py
