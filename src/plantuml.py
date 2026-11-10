PUML_FILE = "graph.puml"


def to_plantuml(graph, cycles=()):
    lines = ["@startuml", "skinparam componentStyle rectangle"]
    for name in graph:
        lines.append('component "%s" as %s' % (name, _alias(name)))
    for name, deps in graph.items():
        for child in deps:
            arrow = "-[#red]->" if _in_cycle(name, child, cycles) else "-->"
            lines.append("%s %s %s" % (_alias(name), arrow, _alias(child)))
    lines.append("@enduml")
    return "\n".join(lines) + "\n"


def save(text, path=PUML_FILE):
    with open(path, "w", encoding="utf-8") as stream:
        stream.write(text)
    return path


def _alias(name):
    return "p_" + "".join(char if char.isalnum() else "_" for char in name)


def _in_cycle(name, child, cycles):
    for cycle in cycles:
        if any(pair == (name, child) for pair in zip(cycle, cycle[1:])):
            return True
    return False
