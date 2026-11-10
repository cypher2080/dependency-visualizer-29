import re

from src.errors import RepositoryError

NAME_PATTERN = re.compile(r"^[A-Z]+$")


def parse_graph(text):
    graph = {}
    for number, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise RepositoryError("строка %d: ожидается 'A: B C'" % number)
        name, deps = line.split(":", 1)
        names = [name.strip()] + deps.split()
        for item in names:
            if not NAME_PATTERN.match(item):
                raise RepositoryError(
                    "строка %d: неверное имя пакета %s" % (number, item))
        graph[names[0]] = names[1:]
    return graph


class LocalRepository:
    def __init__(self, path):
        try:
            with open(path, encoding="utf-8") as stream:
                self.graph = parse_graph(stream.read())
        except OSError:
            raise RepositoryError("не удалось открыть файл " + str(path))

    def dependencies(self, package, version=None):
        known = set(self.graph)
        for deps in self.graph.values():
            known.update(deps)
        if package not in known:
            raise RepositoryError("пакет %s не найден" % package)
        return list(self.graph.get(package, []))
