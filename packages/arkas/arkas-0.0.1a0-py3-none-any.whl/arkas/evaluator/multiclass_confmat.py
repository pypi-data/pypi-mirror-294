r"""Contain the confusion matrix evaluator."""

from __future__ import annotations

__all__ = ["MulticlassConfusionMatrixEvaluator"]

import logging
from typing import TYPE_CHECKING

from arkas.evaluator.base import BaseLazyEvaluator
from arkas.result import EmptyResult, MulticlassConfusionMatrixResult
from arkas.utils.array import to_array
from arkas.utils.data import find_keys, find_missing_keys

if TYPE_CHECKING:
    import polars as pl

    from arkas.result import BaseResult

logger = logging.getLogger(__name__)


class MulticlassConfusionMatrixEvaluator(BaseLazyEvaluator):
    r"""Implement the confusion matrix evaluator for multiclass labels.

    Args:
        y_true: The key or column name of the ground truth target
            labels.
        y_pred: The key or column name of the predicted labels.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> import polars as pl
    >>> from arkas.evaluator import MulticlassConfusionMatrixEvaluator
    >>> data = {"pred": np.array([0, 0, 1, 1, 2, 2]), "target": np.array([0, 0, 1, 1, 2, 2])}
    >>> evaluator = MulticlassConfusionMatrixEvaluator(y_true="target", y_pred="pred")
    >>> evaluator
    MulticlassConfusionMatrixEvaluator(y_true=target, y_pred=pred)
    >>> result = evaluator.evaluate(data)
    >>> result
    MulticlassConfusionMatrixResult(y_true=(6,), y_pred=(6,))

    ```
    """

    def __init__(self, y_true: str, y_pred: str) -> None:
        self._y_true = y_true
        self._y_pred = y_pred

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(y_true={self._y_true}, y_pred={self._y_pred})"

    def _evaluate(self, data: dict | pl.DataFrame) -> BaseResult:
        logger.info(
            f"Evaluating the multiclass confusion matrix | y_true={self._y_true} | "
            f"y_pred={self._y_pred}"
        )
        if missing_keys := find_missing_keys(
            keys=find_keys(data), queries=[self._y_pred, self._y_true]
        ):
            logger.warning(
                "Skipping the multiclass confusion matrix evaluation because some keys "
                f"are missing: {sorted(missing_keys)}"
            )
            return EmptyResult()
        return MulticlassConfusionMatrixResult(
            y_true=to_array(data[self._y_true]).ravel(), y_pred=to_array(data[self._y_pred]).ravel()
        )
