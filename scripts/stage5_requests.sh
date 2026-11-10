#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
python3 -m src.main configs/requests.ini plantuml
