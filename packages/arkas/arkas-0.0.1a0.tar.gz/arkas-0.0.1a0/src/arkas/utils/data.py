r"""Contain data utility functions."""

from __future__ import annotations

__all__ = ["find_keys", "find_missing_keys"]


from typing import TYPE_CHECKING

import polars as pl

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence


def find_keys(data: Mapping | pl.DataFrame) -> set:
    r"""Find all the keys in the input data.

    Args:
        data: The input data.

    Returns:
        The set of keys.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.utils.data import find_keys
    >>> keys = find_keys(
    ...     {"pred": np.array([3, 2, 0, 1, 0]), "target": np.array([3, 2, 0, 1, 0])}
    ... )
    >>> sorted(keys)
    ['pred', 'target']
    >>> keys = find_keys(pl.DataFrame({"pred": [3, 2, 0, 1, 0], "target": [3, 2, 0, 1, 0]}))
    >>> sorted(keys)
    ['pred', 'target']

    ```
    """
    if isinstance(data, pl.DataFrame):
        return set(data.columns)
    return set(data.keys())


def find_missing_keys(keys: set | Sequence, queries: set | Sequence) -> set:
    r"""Return the set of queries that are not in the input keys.

    Args:
        keys: The keys.
        queries: The queries i.e. the keys to check in the input keys.

    Returns:
        The set of missing keys.

    Example usage:

    ```pycon

    >>> from arkas.utils.data import find_missing_keys
    >>> keys = find_missing_keys(
    ...     keys={"key1", "key2", "key3"}, queries=["key1", "key2", "key4"]
    ... )
    >>> keys
    {'key4'}

    ```
    """
    keys = set(keys)
    queries = set(queries)
    intersection = set(keys).intersection(queries)
    return queries.difference(intersection)
