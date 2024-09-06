r"""Contain the F-beta evaluator for binary labels."""

from __future__ import annotations

__all__ = ["BinaryFbetaEvaluator"]

import logging
from typing import TYPE_CHECKING

from arkas.evaluator.base import BaseLazyEvaluator
from arkas.result import BinaryFbetaResult, EmptyResult
from arkas.utils.array import to_array
from arkas.utils.data import find_keys, find_missing_keys

if TYPE_CHECKING:
    from collections.abc import Sequence

    import polars as pl

    from arkas.result import BaseResult

logger = logging.getLogger(__name__)


class BinaryFbetaEvaluator(BaseLazyEvaluator):
    r"""Implement the F-beta evaluator for binary labels.

    Args:
        y_true: The key or column name of the ground truth target
            labels.
        y_pred: The key or column name of the predicted labels.
        betas: The betas used to compute the F-beta scores.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> import polars as pl
    >>> from arkas.evaluator import BinaryFbetaEvaluator
    >>> data = {"pred": np.array([1, 0, 0, 1, 1]), "target": np.array([1, 0, 0, 1, 1])}
    >>> evaluator = BinaryFbetaEvaluator(y_true="target", y_pred="pred")
    >>> evaluator
    BinaryFbetaEvaluator(y_true=target, y_pred=pred, betas=(1,))
    >>> result = evaluator.evaluate(data)
    >>> result
    BinaryFbetaResult(y_true=(5,), y_pred=(5,), betas=(1,))

    ```
    """

    def __init__(self, y_true: str, y_pred: str, betas: Sequence[float] = (1,)) -> None:
        self._y_true = y_true
        self._y_pred = y_pred
        self._betas = tuple(betas)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(y_true={self._y_true}, "
            f"y_pred={self._y_pred}, betas={self._betas})"
        )

    def _evaluate(self, data: dict | pl.DataFrame) -> BaseResult:
        logger.info(
            f"Evaluating the binary F-beta | y_true={self._y_true} | y_pred={self._y_pred} | "
            f"betas={self._betas}"
        )
        if missing_keys := find_missing_keys(
            keys=find_keys(data), queries=[self._y_pred, self._y_true]
        ):
            logger.warning(
                "Skipping the binary F-beta evaluation because some keys are missing: "
                f"{sorted(missing_keys)}"
            )
            return EmptyResult()
        return BinaryFbetaResult(
            y_true=to_array(data[self._y_true]).ravel(),
            y_pred=to_array(data[self._y_pred]).ravel(),
            betas=self._betas,
        )
