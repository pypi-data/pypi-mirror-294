r"""Contain DataFrame utility functions."""

from __future__ import annotations

__all__ = ["to_arrays"]


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np
    import polars as pl


def to_arrays(frame: pl.DataFrame) -> dict[str, np.ndarray]:
    r"""Convert a ``polars.DataFrame`` to a dictionary of NumPy arrays.

    Args:
        frame: The DataFrame to convert.

    Returns:
        A dictionary of NumPy arrays.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from arkas.utils.dataframe import to_arrays
    >>> frame = pl.DataFrame(
    ...     {
    ...         "int": [1, 2, 3, 4, 5],
    ...         "float": [5.0, 4.0, 3.0, 2.0, 1.0],
    ...         "str": ["a", "b", "c", "d", "e"],
    ...     },
    ...     schema={"int": pl.Int64, "float": pl.Float64, "str": pl.String},
    ... )
    >>> data = to_arrays(frame)
    >>> data
    {'int': array([1, 2, 3, 4, 5]),
     'float': array([5., 4., 3., 2., 1.]),
     'str': array(['a', 'b', 'c', 'd', 'e'], dtype=object)}

    ```
    """
    return {s.name: s.to_numpy() for s in frame.iter_columns()}
