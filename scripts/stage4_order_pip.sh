#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
python3 -m src.main configs/flask.ini order
echo "pip install flask==3.0.0:"
cat docs/pip_flask_order.txt
