r"""Contain an evaluator that evaluates a mapping of evaluators."""

from __future__ import annotations

__all__ = ["MappingEvaluator"]

import logging
from typing import TYPE_CHECKING

from coola.utils import repr_indent, repr_mapping

from arkas.evaluator import BaseEvaluator
from arkas.result import EmptyResult, MappingResult, Result

if TYPE_CHECKING:
    from collections.abc import Hashable, Mapping

    import polars as pl

    from arkas.result import BaseResult

logger = logging.getLogger(__name__)


class MappingEvaluator(BaseEvaluator):
    r"""Implement an evaluator that sequentially evaluates a mapping of
    evaluators.

    Args:
        evaluators: The mapping of evaluators to evaluate.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> import polars as pl
    >>> from arkas.evaluator import (
    ...     MappingEvaluator,
    ...     BinaryPrecisionEvaluator,
    ...     BinaryRecallEvaluator,
    ... )
    >>> data = {"pred": np.array([1, 0, 0, 1, 1]), "target": np.array([1, 0, 0, 1, 1])}
    >>> evaluator = MappingEvaluator(
    ...     {
    ...         "precision": BinaryPrecisionEvaluator(y_true="target", y_pred="pred"),
    ...         "recall": BinaryRecallEvaluator(y_true="target", y_pred="pred"),
    ...     }
    ... )
    >>> evaluator
    MappingEvaluator(
      (precision): BinaryPrecisionEvaluator(y_true=target, y_pred=pred)
      (recall): BinaryRecallEvaluator(y_true=target, y_pred=pred)
    )
    >>> result = evaluator.evaluate(data)
    >>> result
    MappingResult(count=2)
    >>> result = evaluator.evaluate(data, lazy=False)
    >>> result
    Result(metrics=2, figures=2)
    >>> frame = pl.DataFrame({"pred": [3, 2, 0, 1, 0, 1], "target": [3, 2, 0, 1, 0, 1]})
    >>> result = evaluator.evaluate(frame)
    >>> result
    MappingResult(count=2)

    ```
    """

    def __init__(self, evaluators: Mapping[Hashable, BaseEvaluator]) -> None:
        self._evaluators = evaluators

    def __repr__(self) -> str:
        args = repr_indent(repr_mapping(self._evaluators))
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def evaluate(self, data: dict | pl.DataFrame, lazy: bool = True) -> BaseResult:
        out = MappingResult(
            {
                key: evaluator.evaluate(data=data, lazy=lazy)
                for key, evaluator in self._evaluators.items()
            }
        )
        if lazy or isinstance(out, EmptyResult):
            return out
        return Result(metrics=out.compute_metrics(), figures=out.generate_figures())
