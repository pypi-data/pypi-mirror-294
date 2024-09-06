r"""Contain an accuracy evaluator."""

from __future__ import annotations

__all__ = ["BalancedAccuracyEvaluator"]

import logging
from typing import TYPE_CHECKING

from arkas.evaluator.base import BaseLazyEvaluator
from arkas.result import BalancedAccuracyResult, EmptyResult
from arkas.utils.array import to_array
from arkas.utils.data import find_keys, find_missing_keys

if TYPE_CHECKING:
    import polars as pl

    from arkas.result import BaseResult

logger = logging.getLogger(__name__)


class BalancedAccuracyEvaluator(BaseLazyEvaluator):
    r"""Implement the accuracy evaluator.

    Args:
        y_true: The key or column name of the ground truth target
            labels.
        y_pred: The key or column name of the predicted labels.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> import polars as pl
    >>> from arkas.evaluator import BalancedAccuracyEvaluator
    >>> data = {"pred": np.array([3, 2, 0, 1, 0]), "target": np.array([3, 2, 0, 1, 0])}
    >>> evaluator = BalancedAccuracyEvaluator(y_true="target", y_pred="pred")
    >>> evaluator
    BalancedAccuracyEvaluator(y_true=target, y_pred=pred)
    >>> result = evaluator.evaluate(data)
    >>> result
    BalancedAccuracyResult(y_true=(5,), y_pred=(5,))
    >>> frame = pl.DataFrame({"pred": [3, 2, 0, 1, 0, 1], "target": [3, 2, 0, 1, 0, 1]})
    >>> result = evaluator.evaluate(frame)
    >>> result
    BalancedAccuracyResult(y_true=(6,), y_pred=(6,))

    ```
    """

    def __init__(self, y_true: str, y_pred: str) -> None:
        self._y_true = y_true
        self._y_pred = y_pred

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(y_true={self._y_true}, y_pred={self._y_pred})"

    def _evaluate(self, data: dict | pl.DataFrame) -> BaseResult:
        logger.info(
            f"Evaluating the balanced accuracy | y_true={self._y_true} | y_pred={self._y_pred}"
        )
        if missing_keys := find_missing_keys(
            keys=find_keys(data), queries=[self._y_pred, self._y_true]
        ):
            logger.warning(
                "Skipping the balanced accuracy evaluation because some keys are missing: "
                f"{sorted(missing_keys)}"
            )
            return EmptyResult()
        return BalancedAccuracyResult(
            y_true=to_array(data[self._y_true]).ravel(), y_pred=to_array(data[self._y_pred]).ravel()
        )
