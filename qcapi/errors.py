from __future__ import annotations
from typing import Optional


class QCException(Exception):
    errors: Optional[list[str]] = None

    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors
