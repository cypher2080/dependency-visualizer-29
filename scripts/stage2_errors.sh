#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
for name in unknown_package unknown_version; do
    echo "== $name.ini"
    python3 -m src.main "configs/errors/$name.ini" deps 2>&1
done
