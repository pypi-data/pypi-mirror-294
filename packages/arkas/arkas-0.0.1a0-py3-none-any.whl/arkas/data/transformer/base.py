r"""Contain the base class to implement a data transformer."""

from __future__ import annotations

__all__ = ["BaseTransformer", "is_transformer_config", "setup_transformer"]

import logging
from abc import ABC

from objectory import AbstractFactory
from objectory.utils import is_object_config

logger = logging.getLogger(__name__)


class BaseTransformer(ABC, metaclass=AbstractFactory):
    r"""Define the base class to transform data.

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

    def transform(self, data: dict) -> dict:
        r"""Transform the data.

        Args:
            data: The data to transform.

        Returns:
            The transformed data.

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


def is_transformer_config(config: dict) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``BaseTransformer``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: The configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration
            for a ``BaseTransformer`` object.

    Example usage:

    ```pycon

    >>> from arkas.data.transformer import is_transformer_config
    >>> is_transformer_config({"_target_": "arkas.data.transformer.DataFrameTransformer"})
    True

    ```
    """
    return is_object_config(config, BaseTransformer)


def setup_transformer(
    transformer: BaseTransformer | dict,
) -> BaseTransformer:
    r"""Set up a data transformer.

    The transformer is instantiated from its configuration
    by using the ``BaseTransformer`` factory function.

    Args:
        transformer: A data transformer or its configuration.

    Returns:
        An instantiated transformer.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from arkas.data.transformer import setup_transformer
    >>> transformer = setup_transformer(
    ...     {
    ...         "_target_": "arkas.data.transformer.DataFrameTransformer",
    ...         "transformer": {
    ...             "_target_": "grizz.transformer.Cast",
    ...             "columns": ("col1", "col3"),
    ...             "dtype": pl.Int32,
    ...         },
    ...         "in_key": "frame",
    ...         "out_key": "frame",
    ...     }
    ... )
    >>> transformer
    DataFrameTransformer(
      (transformer): CastTransformer(columns=('col1', 'col3'), dtype=Int32, ignore_missing=False)
      (in_key): frame
      (out_key): frame
    )

    ```
    """
    if isinstance(transformer, dict):
        logger.info("Initializing a DataFrame transformer from its configuration... ")
        transformer = BaseTransformer.factory(**transformer)
    if not isinstance(transformer, BaseTransformer):
        logger.warning(f"transformer is not a `BaseTransformer` (received: {type(transformer)})")
    return transformer
