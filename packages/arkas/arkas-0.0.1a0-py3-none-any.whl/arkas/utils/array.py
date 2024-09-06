r"""Implement some utility functions for ``numpy.ndarray``s."""

from __future__ import annotations

__all__ = ["to_array"]

from typing import TYPE_CHECKING, Any

import polars as pl
from coola.utils.array import to_array as coola_to_array

if TYPE_CHECKING:
    import numpy as np


def to_array(data: Any) -> np.ndarray:
    r"""Convert the input to a ``numpy.ndarray``.

    Args:
        data: The data to convert to a NumPy array.

    Returns:
        A NumPy array.

    Example usage:

    ```pycon

    >>> from arkas.utils.array import to_array
    >>> x = to_array([1, 2, 3, 4, 5])
    >>> x
    array([1, 2, 3, 4, 5])

    ```
    """
    if isinstance(data, pl.Series):
        return data.to_numpy()
    return coola_to_array(data)
