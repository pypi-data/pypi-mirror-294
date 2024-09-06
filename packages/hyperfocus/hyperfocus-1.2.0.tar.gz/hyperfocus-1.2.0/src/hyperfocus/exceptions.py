from __future__ import annotations


class HyperfocusError(Exception):
    """Hyperfocus base class exception."""

    exit_code = 1

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
