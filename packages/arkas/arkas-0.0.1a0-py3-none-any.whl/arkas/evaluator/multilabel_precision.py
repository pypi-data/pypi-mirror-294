r"""Contain the precision evaluator for multilabel labels."""

from __future__ import annotations

__all__ = ["MultilabelPrecisionEvaluator"]

import logging
from typing import TYPE_CHECKING

from arkas.evaluator.base import BaseLazyEvaluator
from arkas.result import EmptyResult, MultilabelPrecisionResult
from arkas.utils.array import to_array
from arkas.utils.data import find_keys, find_missing_keys

if TYPE_CHECKING:
    import polars as pl

    from arkas.result import BaseResult

logger = logging.getLogger(__name__)


class MultilabelPrecisionEvaluator(BaseLazyEvaluator):
    r"""Implement the precision evaluator for multilabel labels.

    Args:
        y_true: The key or column name of the ground truth target
            labels.
        y_pred: The key or column name of the predicted labels.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> import polars as pl
    >>> from arkas.evaluator import MultilabelPrecisionEvaluator
    >>> data = {
    ...     "pred": np.array([[1, 0, 0], [0, 1, 1], [0, 1, 1], [1, 0, 0], [1, 0, 0]]),
    ...     "target": np.array([[1, 0, 1], [0, 1, 0], [0, 1, 0], [1, 0, 1], [1, 0, 1]]),
    ... }
    >>> evaluator = MultilabelPrecisionEvaluator(y_true="target", y_pred="pred")
    >>> evaluator
    MultilabelPrecisionEvaluator(y_true=target, y_pred=pred)
    >>> result = evaluator.evaluate(data)
    >>> result
    MultilabelPrecisionResult(y_true=(5, 3), y_pred=(5, 3))

    ```
    """

    def __init__(self, y_true: str, y_pred: str) -> None:
        self._y_true = y_true
        self._y_pred = y_pred

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(y_true={self._y_true}, y_pred={self._y_pred})"

    def _evaluate(self, data: dict | pl.DataFrame) -> BaseResult:
        logger.info(
            f"Evaluating the multilabel precision | y_true={self._y_true} | y_pred={self._y_pred}"
        )
        if missing_keys := find_missing_keys(
            keys=find_keys(data), queries=[self._y_pred, self._y_true]
        ):
            logger.warning(
                "Skipping the multilabel precision evaluation because some keys are missing: "
                f"{sorted(missing_keys)}"
            )
            return EmptyResult()
        return MultilabelPrecisionResult(
            y_true=to_array(data[self._y_true]), y_pred=to_array(data[self._y_pred])
        )
