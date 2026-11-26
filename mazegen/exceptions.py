class ParserError(Exception):
    """Raise when a line of the config file is malformed."""

class MazeConfigError(Exception):
    """Raise when the config values are incoherent or cannot be used."""

class MazeInternalError(Exception):
    """Raise when the maze logic reaches an unexpected inconsistent state."""
