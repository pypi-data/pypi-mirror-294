r"""Contain an evaluator that sequentially evaluates several
evaluators."""

from __future__ import annotations

__all__ = ["SequentialEvaluator"]

import logging
from typing import TYPE_CHECKING

from coola.utils import repr_indent, repr_sequence

from arkas.evaluator import BaseEvaluator
from arkas.result import EmptyResult, Result, SequentialResult

if TYPE_CHECKING:
    from collections.abc import Sequence

    import polars as pl

    from arkas.result import BaseResult

logger = logging.getLogger(__name__)


class SequentialEvaluator(BaseEvaluator):
    r"""Implement an evaluator that sequentially evaluates several
    evaluators.

    Args:
        evaluators: The sequence of evaluators to evaluate.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> import polars as pl
    >>> from arkas.evaluator import (
    ...     SequentialEvaluator,
    ...     BinaryPrecisionEvaluator,
    ...     BinaryRecallEvaluator,
    ... )
    >>> data = {"pred": np.array([1, 0, 0, 1, 1]), "target": np.array([1, 0, 0, 1, 1])}
    >>> evaluator = SequentialEvaluator(
    ...     [
    ...         BinaryPrecisionEvaluator(y_true="target", y_pred="pred"),
    ...         BinaryRecallEvaluator(y_true="target", y_pred="pred"),
    ...     ]
    ... )
    >>> evaluator
    SequentialEvaluator(
      (0): BinaryPrecisionEvaluator(y_true=target, y_pred=pred)
      (1): BinaryRecallEvaluator(y_true=target, y_pred=pred)
    )
    >>> result = evaluator.evaluate(data)
    >>> result
    SequentialResult(count=2)
    >>> result = evaluator.evaluate(data, lazy=False)
    >>> result
    Result(metrics=3, figures=1)
    >>> frame = pl.DataFrame({"pred": [3, 2, 0, 1, 0, 1], "target": [3, 2, 0, 1, 0, 1]})
    >>> result = evaluator.evaluate(frame)
    >>> result
    SequentialResult(count=2)

    ```
    """

    def __init__(self, evaluators: Sequence[BaseEvaluator]) -> None:
        self._evaluators = tuple(evaluators)

    def __repr__(self) -> str:
        args = repr_indent(repr_sequence(self._evaluators))
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def evaluate(self, data: dict | pl.DataFrame, lazy: bool = True) -> BaseResult:
        out = SequentialResult(
            [evaluator.evaluate(data=data, lazy=lazy) for evaluator in self._evaluators]
        )
        if lazy or isinstance(out, EmptyResult):
            return out
        return Result(metrics=out.compute_metrics(), figures=out.generate_figures())
