r"""Contain the average precision evaluator for binary labels."""

from __future__ import annotations

__all__ = ["BinaryClassificationEvaluator"]

import logging
from typing import TYPE_CHECKING

from arkas.evaluator.base import BaseLazyEvaluator
from arkas.result import BinaryClassificationResult, EmptyResult
from arkas.utils.array import to_array
from arkas.utils.data import find_keys, find_missing_keys

if TYPE_CHECKING:
    import polars as pl

    from arkas.result import BaseResult

logger = logging.getLogger(__name__)


class BinaryClassificationEvaluator(BaseLazyEvaluator):
    r"""Implement the average precision evaluator for binary labels.

    Args:
        y_true: The key or column name of the ground truth target
            labels.
        y_pred: The key or column name of the predicted labels.
        y_score: The target scores, can either be probability
            estimates of the positive class, confidence values,
            or non-thresholded measure of decisions.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> import polars as pl
    >>> from arkas.evaluator import BinaryClassificationEvaluator
    >>> data = {
    ...     "pred": np.array([1, 0, 0, 1, 1]),
    ...     "score": np.array([2, -1, 0, 3, 1]),
    ...     "target": np.array([1, 0, 0, 1, 1]),
    ... }
    >>> evaluator = BinaryClassificationEvaluator(
    ...     y_true="target", y_pred="pred", y_score="score"
    ... )
    >>> evaluator
    BinaryClassificationEvaluator(y_true=target, y_pred=pred, y_score=score)
    >>> result = evaluator.evaluate(data)
    >>> result
    BinaryClassificationResult(y_true=(5,), y_pred=(5,), y_score=(5,), betas=(1,))

    ```
    """

    def __init__(self, y_true: str, y_pred: str, y_score: str | None = None) -> None:
        self._y_true = y_true
        self._y_pred = y_pred
        self._y_score = y_score

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(y_true={self._y_true}, y_pred={self._y_pred}, "
            f"y_score={self._y_score})"
        )

    def _evaluate(self, data: dict | pl.DataFrame) -> BaseResult:
        logger.info(
            f"Evaluating the binary average precision | y_true={self._y_true} | "
            f"y_pred={self._y_pred} | y_score={self._y_score}"
        )
        if missing_keys := find_missing_keys(keys=find_keys(data), queries=self._get_keys()):
            logger.warning(
                "Skipping the binary average precision evaluation because some keys are missing: "
                f"{sorted(missing_keys)}"
            )
            return EmptyResult()
        return BinaryClassificationResult(
            y_true=to_array(data[self._y_true]).ravel(),
            y_pred=to_array(data[self._y_pred]).ravel(),
            y_score=to_array(data[self._y_score]).ravel() if self._y_score is not None else None,
        )

    def _get_keys(self) -> list[str]:
        keys = [self._y_pred, self._y_true]
        if self._y_score is not None:
            keys.append(self._y_score)
        return keys
