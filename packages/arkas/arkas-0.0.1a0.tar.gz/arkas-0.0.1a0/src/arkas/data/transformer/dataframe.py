r"""Contain a DataFrame transformer."""

from __future__ import annotations

__all__ = ["DataFrameTransformer"]

from coola.utils import repr_indent, repr_mapping, str_indent, str_mapping
from grizz.transformer import BaseTransformer as GBaseTransformer
from grizz.transformer import setup_transformer

from arkas.data.transformer import BaseTransformer


class DataFrameTransformer(BaseTransformer):
    r"""Implement a data transformer to transform a DataFrame.

    Args:
        transformer: The DataFrame transformer or its configuration.
        in_key: The key of the DataFrame to transform in the input
            dictionary.
        out_key: The key of the transformed DataFrame in the output
            dictionary.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.transformer import Cast
    >>> from arkas.data.transformer import DataFrameTransformer
    >>> frame = pl.DataFrame(
    ...     {
    ...         "col1": [1, 2, 3, 4, 5],
    ...         "col2": ["1", "2", "3", "4", "5"],
    ...         "col3": ["a", "b", "c", "d", "e"],
    ...     }
    ... )
    >>> transformer = DataFrameTransformer(
    ...     transformer=Cast(columns=["col2"], dtype=pl.Int64), in_key="frame", out_key="frame"
    ... )
    >>> transformer
    DataFrameTransformer(
      (transformer): CastTransformer(columns=('col2',), dtype=Int64, ignore_missing=False)
      (in_key): frame
      (out_key): frame
    )
    >>> data = transformer.transform({"frame": frame})
    >>> data
    {'frame': shape: (5, 3)
    ┌──────┬──────┬──────┐
    │ col1 ┆ col2 ┆ col3 │
    │ ---  ┆ ---  ┆ ---  │
    │ i64  ┆ i64  ┆ str  │
    ╞══════╪══════╪══════╡
    │ 1    ┆ 1    ┆ a    │
    │ 2    ┆ 2    ┆ b    │
    │ 3    ┆ 3    ┆ c    │
    │ 4    ┆ 4    ┆ d    │
    │ 5    ┆ 5    ┆ e    │
    └──────┴──────┴──────┘}

    ```
    """

    def __init__(self, transformer: GBaseTransformer | dict, in_key: str, out_key: str) -> None:
        self._transformer = setup_transformer(transformer)
        self._in_key = in_key
        self._out_key = out_key

    def __repr__(self) -> str:
        args = repr_indent(
            repr_mapping(
                {
                    "transformer": self._transformer,
                    "in_key": self._in_key,
                    "out_key": self._out_key,
                }
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def __str__(self) -> str:
        args = str_indent(
            str_mapping(
                {
                    "transformer": self._transformer,
                    "in_key": self._in_key,
                    "out_key": self._out_key,
                }
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def transform(self, data: dict) -> dict:
        data = data.copy()
        data[self._out_key] = self._transformer.transform(data[self._in_key])
        return data
