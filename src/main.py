import sys

from src.config import load_config
from src.errors import VisualizerError
from src.graph import build_graph, load_order
from src.local_repo import LocalRepository
from src.plantuml import save, to_plantuml
from src.pypi import PypiRepository

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


def open_repository(config):
    if config.test_mode:
        return LocalRepository(config.repository)
    return PypiRepository(config.repository)


def make_graph(config):
    return build_graph(
        open_repository(config), config.package, config.max_depth,
        config.exclude, config.version)


def show_deps(config):
    repository = open_repository(config)
    names = repository.dependencies(config.package, config.version)
    print("Прямые зависимости %s %s:" % (config.package, config.version))
    for name in names:
        print("  " + name)


def show_graph(config):
    graph, cycles = make_graph(config)
    print("Граф зависимостей %s:" % config.package)
    for name, deps in graph.items():
        print("  %s -> %s" % (name, ", ".join(deps) or "-"))
    for cycle in cycles:
        print("Цикл: " + " -> ".join(cycle))


def show_order(config):
    graph, cycles = make_graph(config)
    print("Порядок загрузки: " + " ".join(load_order(graph, config.package)))
    if cycles:
        print("Циклы разорваны при обходе: %d" % len(cycles))


def show_plantuml(config):
    graph, cycles = make_graph(config)
    text = to_plantuml(graph, cycles)
    print(text, end="")
    print("Сохранено в " + save(text))


MODES = {
    "params": show_params,
    "deps": show_deps,
    "graph": show_graph,
    "order": show_order,
    "plantuml": show_plantuml,
}


if __name__ == "__main__":
    sys.exit(main())
