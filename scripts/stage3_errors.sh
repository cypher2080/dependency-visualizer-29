#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
echo "== no_test_file.ini"
python3 -m src.main configs/errors/no_test_file.ini graph 2>&1
