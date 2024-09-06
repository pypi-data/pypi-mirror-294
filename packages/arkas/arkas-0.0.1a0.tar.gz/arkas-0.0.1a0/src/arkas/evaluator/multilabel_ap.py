r"""Contain the average precision evaluator for multilabel labels."""

from __future__ import annotations

__all__ = ["MultilabelAveragePrecisionEvaluator"]

import logging
from typing import TYPE_CHECKING

from arkas.evaluator.base import BaseLazyEvaluator
from arkas.result import EmptyResult, MultilabelAveragePrecisionResult
from arkas.utils.array import to_array
from arkas.utils.data import find_keys, find_missing_keys

if TYPE_CHECKING:
    import polars as pl

    from arkas.result import BaseResult

logger = logging.getLogger(__name__)


class MultilabelAveragePrecisionEvaluator(BaseLazyEvaluator):
    r"""Implement the average precision evaluator for multilabel labels.

    Args:
        y_true: The key or column name of the ground truth target
            labels.
        y_score: The target scores, can either be probability
            estimates of the positive class, confidence values,
            or non-thresholded measure of decisions.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> import polars as pl
    >>> from arkas.evaluator import MultilabelAveragePrecisionEvaluator
    >>> data = {
    ...     "pred": np.array([[2, -1, 1], [-1, 1, -2], [0, 2, -3], [3, -2, 4], [1, -3, 5]]),
    ...     "target": np.array([[1, 0, 1], [0, 1, 0], [0, 1, 0], [1, 0, 1], [1, 0, 1]]),
    ... }
    >>> evaluator = MultilabelAveragePrecisionEvaluator(y_true="target", y_score="pred")
    >>> evaluator
    MultilabelAveragePrecisionEvaluator(y_true=target, y_score=pred)
    >>> result = evaluator.evaluate(data)
    >>> result
    MultilabelAveragePrecisionResult(y_true=(5, 3), y_score=(5, 3))

    ```
    """

    def __init__(self, y_true: str, y_score: str) -> None:
        self._y_true = y_true
        self._y_score = y_score

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(y_true={self._y_true}, y_score={self._y_score})"

    def _evaluate(self, data: dict | pl.DataFrame) -> BaseResult:
        logger.info(
            f"Evaluating the multilabel average precision | y_true={self._y_true} | y_score={self._y_score}"
        )
        if missing_keys := find_missing_keys(
            keys=find_keys(data), queries=[self._y_score, self._y_true]
        ):
            logger.warning(
                "Skipping the multilabel average precision evaluation because some keys are missing: "
                f"{sorted(missing_keys)}"
            )
            return EmptyResult()
        return MultilabelAveragePrecisionResult(
            y_true=to_array(data[self._y_true]), y_score=to_array(data[self._y_score])
        )
