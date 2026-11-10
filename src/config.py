import configparser
import re

from src.errors import ConfigError

SECTION = "settings"
KEYS = (
    "package", "version", "repository", "test_mode", "max_depth", "exclude")
LATEST = "latest"
VERSION_PATTERN = re.compile(r"^\d+(\.\d+)*([a-z]+\d*)?(\.post\d+)?$")
MIN_DEPTH = 1


class Config:
    def __init__(self, values):
        for key in KEYS:
            setattr(self, key, values[key])

    def items(self):
        return [(key, getattr(self, key)) for key in KEYS]


def load_config(path):
    parser = configparser.ConfigParser()
    try:
        with open(path, encoding="utf-8") as stream:
            parser.read_file(stream)
    except OSError:
        raise ConfigError("не удалось открыть файл " + str(path))
    except configparser.MissingSectionHeaderError:
        raise ConfigError("нет секции [%s]" % SECTION)
    except configparser.ParsingError as error:
        raise ConfigError(
            "строка %d: ожидается 'ключ = значение'" % error.errors[0][0])
    except configparser.Error as error:
        raise ConfigError("неверный формат INI: " + error.message)
    if not parser.has_section(SECTION):
        raise ConfigError("нет секции [%s]" % SECTION)
    return build_config(dict(parser.items(SECTION)))


def build_config(data):
    for key in data:
        if key not in KEYS:
            raise ConfigError("неизвестный параметр " + key)
    return Config({
        "package": _package(data),
        "version": _version(data.get("version", LATEST)),
        "repository": _required(data, "repository"),
        "test_mode": _bool(data),
        "max_depth": _depth(data.get("max_depth", "")),
        "exclude": data.get("exclude", ""),
    })


def _required(data, key):
    value = data.get(key, "").strip()
    if not value:
        raise ConfigError("не задан параметр " + key)
    return value


def _package(data):
    name = _required(data, "package")
    if any(char.isspace() for char in name):
        raise ConfigError("имя пакета не должно содержать пробелов")
    return name


def _version(value):
    value = value.strip() or LATEST
    if value != LATEST and not VERSION_PATTERN.match(value):
        raise ConfigError("неверная версия " + value)
    return value


def _bool(data):
    value = data.get("test_mode", "false").lower()
    states = configparser.ConfigParser.BOOLEAN_STATES
    if value not in states:
        raise ConfigError("test_mode должен быть true или false")
    return states[value]


def _depth(value):
    try:
        depth = int(value)
    except ValueError:
        raise ConfigError("max_depth должен быть целым числом")
    if depth < MIN_DEPTH:
        raise ConfigError("max_depth должен быть не меньше 1")
    return depth
