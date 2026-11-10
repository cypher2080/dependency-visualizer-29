#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
python3 -m src.main configs/cycle.ini graph
python3 -m src.main configs/multi_cycle.ini graph
