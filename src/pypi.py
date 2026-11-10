import json
import re
import urllib.error
import urllib.request

from src.errors import RepositoryError

NAME_PATTERN = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)")
EXTRA_PATTERN = re.compile(r"extra\s*==")
LATEST = "latest"
TIMEOUT = 15


def normalize(name):
    return re.sub(r"[-_.]+", "-", name).lower()


def parse_requirement(text):
    if ";" in text and EXTRA_PATTERN.search(text.split(";", 1)[1]):
        return None
    match = NAME_PATTERN.match(text)
    return normalize(match.group(1)) if match else None


def requirements_to_names(requirements):
    names = []
    for text in requirements or []:
        name = parse_requirement(text)
        if name and name not in names:
            names.append(name)
    return names


class PypiRepository:
    def __init__(self, url):
        self.url = url.rstrip("/")
        self.cache = {}

    def dependencies(self, package, version=LATEST):
        key = (package, version)
        if key not in self.cache:
            info = self._load(package, version).get("info", {})
            self.cache[key] = requirements_to_names(info.get("requires_dist"))
        return list(self.cache[key])

    def _load(self, package, version):
        url = "%s/%s/json" % (self.url, package)
        if version != LATEST:
            url = "%s/%s/%s/json" % (self.url, package, version)
        try:
            with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            raise RepositoryError("пакет %s версии %s не найден (HTTP %d)"
                                  % (package, version, error.code))
        except (urllib.error.URLError, OSError, ValueError) as error:
            raise RepositoryError("ошибка запроса %s: %s" % (url, error))
