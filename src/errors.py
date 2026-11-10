class VisualizerError(Exception):
    pass


class ConfigError(VisualizerError):
    pass


class RepositoryError(VisualizerError):
    pass
