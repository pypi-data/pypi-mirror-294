r"""Contain a column to array transformer."""

from __future__ import annotations

__all__ = ["ColumnToArrayTransformer"]

from coola.utils.format import repr_mapping_line, str_mapping_line

from arkas.data.transformer import BaseTransformer


class ColumnToArrayTransformer(BaseTransformer):
    r"""Implement a data transformer that takes a column from a DataFrame
    and convert it to a numpy array.

    Args:
        col: The column name to extract.
        in_key: The key of the DataFrame in the input dictionary.
        out_key: The key of the array in the output dictionary.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.transformer import Cast
    >>> from arkas.data.transformer import ColumnToArrayTransformer
    >>> frame = pl.DataFrame(
    ...     {
    ...         "col1": [1, 2, 3, 4, 5],
    ...         "col2": ["1", "2", "3", "4", "5"],
    ...         "col3": ["a", "b", "c", "d", "e"],
    ...     }
    ... )
    >>> transformer = ColumnToArrayTransformer(col="col1", in_key="frame", out_key="label")
    >>> transformer
    ColumnToArrayTransformer(col='col1', in_key='frame', out_key='label')
    >>> data = transformer.transform({"frame": frame})
    >>> data
    {'frame': shape: (5, 3)
    ┌──────┬──────┬──────┐
    │ col1 ┆ col2 ┆ col3 │
    │ ---  ┆ ---  ┆ ---  │
    │ i64  ┆ str  ┆ str  │
    ╞══════╪══════╪══════╡
    │ 1    ┆ 1    ┆ a    │
    │ 2    ┆ 2    ┆ b    │
    │ 3    ┆ 3    ┆ c    │
    │ 4    ┆ 4    ┆ d    │
    │ 5    ┆ 5    ┆ e    │
    └──────┴──────┴──────┘, 'label': array([1, 2, 3, 4, 5])}

    ```
    """

    def __init__(self, col: str, in_key: str, out_key: str) -> None:
        self._col = col
        self._in_key = in_key
        self._out_key = out_key

    def __repr__(self) -> str:
        args = repr_mapping_line(
            {
                "col": self._col,
                "in_key": self._in_key,
                "out_key": self._out_key,
            }
        )
        return f"{self.__class__.__qualname__}({args})"

    def __str__(self) -> str:
        args = str_mapping_line(
            {
                "col": self._col,
                "in_key": self._in_key,
                "out_key": self._out_key,
            }
        )
        return f"{self.__class__.__qualname__}({args})"

    def transform(self, data: dict) -> dict:
        data = data.copy()
        data[self._out_key] = data[self._in_key][self._col].to_numpy()
        return data
