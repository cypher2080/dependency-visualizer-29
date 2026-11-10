import sys

from src.config import load_config
from src.errors import VisualizerError

DEFAULT_CONFIG = "config.ini"
DEFAULT_MODE = "params"
FAILURE_CODE = 1


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    path = argv[0] if argv else DEFAULT_CONFIG
    mode = argv[1] if len(argv) > 1 else DEFAULT_MODE
    try:
        if mode not in MODES:
            raise VisualizerError("неизвестный режим " + mode)
        MODES[mode](load_config(path))
    except VisualizerError as error:
        print("Ошибка: " + str(error), file=sys.stderr)
        return FAILURE_CODE
    return 0


def show_params(config):
    for key, value in config.items():
        print("%s = %s" % (key, value))


MODES = {
    "params": show_params,
}


if __name__ == "__main__":
    sys.exit(main())
