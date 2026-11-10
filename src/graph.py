LATEST = "latest"


class GraphBuilder:
    def __init__(self, repository, max_depth, exclude=""):
        self.repository = repository
        self.max_depth = max_depth
        self.exclude = exclude
        self.graph = {}
        self.depths = {}
        self.cycles = []
        self.path = []

    def build(self, root, version=LATEST):
        self._visit(root, 0, version)
        return self.graph

    def _visit(self, name, depth, version=LATEST):
        if name in self.path:
            self._add_cycle(name)
            return
        if name in self.depths and self.depths[name] <= depth:
            return
        self.depths[name] = depth
        self.graph[name] = []
        if depth >= self.max_depth:
            return
        self.path.append(name)
        for child in self.repository.dependencies(name, version):
            if self.exclude and self.exclude in child:
                continue
            self.graph[name].append(child)
            self._visit(child, depth + 1)
        self.path.pop()

    def _add_cycle(self, name):
        cycle = self.path[self.path.index(name):] + [name]
        if cycle not in self.cycles:
            self.cycles.append(cycle)


def build_graph(repository, root, max_depth, exclude="", version=LATEST):
    builder = GraphBuilder(repository, max_depth, exclude)
    graph = builder.build(root, version)
    return graph, builder.cycles


def load_order(graph, root):
    order = []
    active = set()

    def visit(name):
        if name in order or name in active:
            return
        active.add(name)
        for child in graph.get(name, []):
            visit(child)
        active.discard(name)
        order.append(name)

    visit(root)
    return order
