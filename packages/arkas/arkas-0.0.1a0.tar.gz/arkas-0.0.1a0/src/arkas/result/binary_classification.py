r"""Implement the default binary classification result."""

from __future__ import annotations

__all__ = ["BinaryClassificationResult"]

from typing import TYPE_CHECKING, Any

from coola import objects_are_equal
from coola.utils.format import repr_mapping_line

from arkas.result.accuracy import AccuracyResult, BalancedAccuracyResult
from arkas.result.ap import BinaryAveragePrecisionResult
from arkas.result.base import BaseResult
from arkas.result.confmat import BinaryConfusionMatrixResult
from arkas.result.fbeta import BinaryFbetaResult
from arkas.result.jaccard import BinaryJaccardResult
from arkas.result.precision import BinaryPrecisionResult
from arkas.result.recall import BinaryRecallResult
from arkas.result.roc_auc import BinaryRocAucResult
from arkas.result.sequential import SequentialResult

if TYPE_CHECKING:
    from collections.abc import Sequence

    import numpy as np


class BinaryClassificationResult(BaseResult):
    r"""Implement the default binary classification result.

    Args:
        y_true: The ground truth target binary labels. This input must
            be an array of shape ``(n_samples,)`` where the values
            are ``0`` or ``1``.
        y_pred: The predicted binary labels. This input must be an
            array of shape ``(n_samples,)`` where the values are ``0``
            or ``1``.
        y_score: The target scores, can either be probability
            estimates of the positive class, confidence values,
            or non-thresholded measure of decisions.
        betas: The betas used to compute the F-beta scores.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.result import BinaryClassificationResult
    >>> result = BinaryClassificationResult(
    ...     y_true=np.array([1, 0, 0, 1, 1]),
    ...     y_pred=np.array([1, 0, 0, 1, 1]),
    ...     y_score=np.array([2, -1, 0, 3, 1]),
    ... )
    >>> result
    BinaryClassificationResult(y_true=(5,), y_pred=(5,), y_score=(5,), betas=(1,))
    >>> result.compute_metrics()
    {'accuracy': 1.0,
     'count_correct': 5,
     'count_incorrect': 0,
     'count': 5,
     'error': 0.0,
     'balanced_accuracy': 1.0,
     'confusion_matrix': array([[2, 0], [0, 3]]),
     'false_negative_rate': 0.0,
     'false_negative': 0,
     'false_positive_rate': 0.0,
     'false_positive': 0,
     'true_negative_rate': 1.0,
     'true_negative': 2,
     'true_positive_rate': 1.0,
     'true_positive': 3,
     'f1': 1.0,
     'jaccard': 1.0,
     'precision': 1.0,
     'recall': 1.0,
     'average_precision': 1.0,
     'roc_auc': 1.0}

    ```
    """

    def __init__(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_score: np.ndarray | None = None,
        betas: Sequence[float] = (1,),
    ) -> None:
        self._y_true = y_true.ravel()
        self._y_pred = y_pred.ravel()
        self._y_score = None if y_score is None else y_score.ravel()
        self._betas = tuple(betas)

        results = [
            AccuracyResult(y_true=self._y_true, y_pred=self._y_pred),
            BalancedAccuracyResult(y_true=self._y_true, y_pred=self._y_pred),
            BinaryConfusionMatrixResult(y_true=self._y_true, y_pred=self._y_pred),
            BinaryFbetaResult(y_true=self._y_true, y_pred=self._y_pred, betas=self._betas),
            BinaryJaccardResult(y_true=self._y_true, y_pred=self._y_pred),
            BinaryPrecisionResult(y_true=self._y_true, y_pred=self._y_pred),
            BinaryRecallResult(y_true=self._y_true, y_pred=self._y_pred),
        ]
        if self._y_score is not None:
            results.extend(
                [
                    BinaryAveragePrecisionResult(y_true=self._y_true, y_score=self._y_score),
                    BinaryRocAucResult(y_true=self._y_true, y_score=self._y_score),
                ]
            )
        self._results = SequentialResult(results)

    def __repr__(self) -> str:
        args = repr_mapping_line(
            {
                "y_true": self._y_true.shape,
                "y_pred": self._y_pred.shape,
                "y_score": self._y_score.shape if self._y_score is not None else None,
                "betas": self._betas,
            }
        )
        return f"{self.__class__.__qualname__}({args})"

    @property
    def y_true(self) -> np.ndarray:
        return self._y_true

    @property
    def y_pred(self) -> np.ndarray:
        return self._y_pred

    @property
    def y_score(self) -> np.ndarray | None:
        return self._y_score

    def compute_metrics(self, prefix: str = "", suffix: str = "") -> dict[str, float]:
        return self._results.compute_metrics(prefix=prefix, suffix=suffix)

    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return (
            objects_are_equal(self.y_true, other.y_true, equal_nan=equal_nan)
            and objects_are_equal(self.y_pred, other.y_pred, equal_nan=equal_nan)
            and objects_are_equal(self.y_score, other.y_score, equal_nan=equal_nan)
            and objects_are_equal(self._betas, other._betas, equal_nan=equal_nan)
        )

    def generate_figures(self, prefix: str = "", suffix: str = "") -> dict[str, float]:
        return self._results.generate_figures(prefix=prefix, suffix=suffix)
