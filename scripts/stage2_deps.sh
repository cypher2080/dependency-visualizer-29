#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
for name in requests flask httpx; do
    python3 -m src.main "configs/$name.ini" deps
done
