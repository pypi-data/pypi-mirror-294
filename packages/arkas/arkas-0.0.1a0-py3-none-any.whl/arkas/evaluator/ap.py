r"""Contain an average precision evaluator."""

from __future__ import annotations

__all__ = ["AveragePrecisionEvaluator"]

import logging
from typing import TYPE_CHECKING

from arkas.evaluator.base import BaseLazyEvaluator
from arkas.result import AveragePrecisionResult, EmptyResult
from arkas.utils.array import to_array
from arkas.utils.data import find_keys, find_missing_keys

if TYPE_CHECKING:
    import polars as pl

    from arkas.result import BaseResult

logger = logging.getLogger(__name__)


class AveragePrecisionEvaluator(BaseLazyEvaluator):
    r"""Implement the average precision evaluator.

    Args:
        y_true: The key or column name of the ground truth target
            labels.
        y_score: The key or column name of the predicted labels.
        label_type: The type of labels used to evaluate the metrics.
            The valid values are: ``'binary'``, ``'multiclass'``,
            ``'multilabel'``, and ``'auto'``. If ``'auto'``, it tries
            to automatically find the label type from the arrays'
            shape.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> import polars as pl
    >>> from arkas.evaluator import AveragePrecisionEvaluator
    >>> data = {"pred": np.array([2, -1, 0, 3, 1]), "target": np.array([1, 0, 0, 1, 1])}
    >>> evaluator = AveragePrecisionEvaluator(y_true="target", y_score="pred")
    >>> evaluator
    AveragePrecisionEvaluator(y_true=target, y_score=pred, label_type=auto)
    >>> result = evaluator.evaluate(data)
    >>> result
    AveragePrecisionResult(y_true=(5,), y_score=(5,), label_type=binary)
    >>> frame = pl.DataFrame({"pred": [2, -1, 0, 3, 1], "target": [1, 0, 0, 1, 1]})
    >>> result = evaluator.evaluate(frame)
    >>> result
    AveragePrecisionResult(y_true=(5,), y_score=(5,), label_type=binary)

    ```
    """

    def __init__(self, y_true: str, y_score: str, label_type: str = "auto") -> None:
        self._y_true = y_true
        self._y_score = y_score
        self._label_type = label_type

        if self._label_type not in {"auto", "binary", "multiclass", "multilabel"}:
            msg = (
                f"Incorrect label type: '{self._label_type}'. The supported label types are: "
                f"'auto', 'binary', 'multiclass', 'multilabel'"
            )
            raise ValueError(msg)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(y_true={self._y_true}, "
            f"y_score={self._y_score}, label_type={self._label_type})"
        )

    def _evaluate(self, data: dict | pl.DataFrame) -> BaseResult:
        logger.info(
            f"Evaluating the average precision | label_type={self._label_type} | "
            f"y_true={self._y_true} | y_score={self._y_score}"
        )
        if missing_keys := find_missing_keys(
            keys=find_keys(data), queries=[self._y_score, self._y_true]
        ):
            logger.warning(
                "Skipping the average precision evaluation because some keys are missing: "
                f"{sorted(missing_keys)}"
            )
            return EmptyResult()
        return AveragePrecisionResult(
            y_true=to_array(data[self._y_true]),
            y_score=to_array(data[self._y_score]),
            label_type=self._label_type,
        )
