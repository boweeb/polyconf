from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Any


@dataclass
class Status(StrEnum):
    NEW = auto()
    OK = auto()
    ERROR = auto()
    WARNING = auto()
    UNKNOWN = auto()
    SKIP = auto()
    RETRY = auto()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self._name_}"

    def __eq__(self, other: Any) -> bool:
        return str(self) == str(other)


def status_new() -> Status:
    return Status.NEW
