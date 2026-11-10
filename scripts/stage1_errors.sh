#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
for name in missing no_section bad_format no_package \
    no_repository bad_version bad_mode bad_depth zero_depth unknown_key; do
    echo "== $name.ini"
    python3 -m src.main "configs/errors/$name.ini" params 2>&1
done
