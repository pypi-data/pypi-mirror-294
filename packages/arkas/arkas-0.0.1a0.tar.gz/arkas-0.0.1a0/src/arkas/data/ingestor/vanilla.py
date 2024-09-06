r"""Contain the implementation of a simple ingestor."""

from __future__ import annotations

__all__ = ["Ingestor"]


from arkas.data.ingestor.base import BaseIngestor


class Ingestor(BaseIngestor):
    r"""Implement a simple data ingestor.

    Args:
        data: The data to ingest.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.data.ingestor import Ingestor
    >>> ingestor = Ingestor(
    ...     data={"pred": np.array([3, 2, 0, 1, 0]), "target": np.array([3, 2, 0, 1, 0])}
    ... )
    >>> ingestor
    Ingestor(num_items=2)
    >>> data = ingestor.ingest()
    >>> data
    {'pred': array([3, 2, 0, 1, 0]), 'target': array([3, 2, 0, 1, 0])}

    ```
    """

    def __init__(self, data: dict) -> None:
        self._data = data

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(num_items={len(self._data):,})"

    def ingest(self) -> dict:
        return self._data.copy()
