#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
for name in simple cycle multi_cycle depth exclude; do
    echo "== $name.ini"
    python3 -m src.main "configs/$name.ini" order
done
