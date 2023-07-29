"""Deep Merge.

Inspired by https://github.com/toumorokoshi/deepmerge. See "Credit" section of the polyconf README.
"""

from __future__ import annotations

from typing import Any, Protocol


# pylint: disable=too-few-public-methods
class Strategy(Protocol):
    """A function that merges two sources."""

    def __call__(
        self,
        merger: Merger,
        path: list[str],
        base: dict[str, Any],
        other: dict[str, Any],
    ) -> dict[str, Any]:
        ...


def dict_strategy_merge(merger: Merger, path: list[str], base: dict[str, Any], other: dict[str, Any]) -> dict[str, Any]:
    """
    For keys that do not exist, use them directly.
    If the key exists in both dictionaries, attempt a value merge.
    """
    for k, v in other.items():
        if k not in base:
            base[k] = v
        else:
            base[k] = merger.value_strategy(path=path + [k], base=base[k], other=v)
    return base


strategy_map: dict[type, Strategy] = {
    list: lambda merger, path, base, other: base + other,  # (list append)
    dict: dict_strategy_merge,
    set: lambda merger, path, base, other: base | other,  # (set union)
}


class Merger:
    """Deep Merge."""

    def merge(self, base: dict[str, Any], other: dict[str, Any]) -> dict[str, Any]:
        """Merge two dictionaries."""
        return self.value_strategy(path=[], base=base, other=other)

    def value_strategy(self, path: list[str], base: dict[str, Any], other: dict[str, Any]) -> dict[str, Any]:
        """Merge two values."""

        # Mismatch types -- other overrides base
        if not (isinstance(base, type(other)) or isinstance(other, type(base))):
            return other

        # Execute strategy
        if strategy := strategy_map.get(type(other)):
            return strategy(self, path, base, other)

        # Fall back to other
        return other


deep = Merger()
