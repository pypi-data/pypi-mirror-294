r"""Implement the confusion matrix results."""

from __future__ import annotations

__all__ = [
    "BaseConfusionMatrixResult",
    "BinaryConfusionMatrixResult",
    "MulticlassConfusionMatrixResult",
    "MultilabelConfusionMatrixResult",
]

from typing import TYPE_CHECKING, Any

from coola import objects_are_equal

from arkas.metric.confmat import (
    binary_confusion_matrix_metrics,
    multiclass_confusion_matrix_metrics,
    multilabel_confusion_matrix_metrics,
)
from arkas.metric.utils import check_same_shape_pred
from arkas.result.base import BaseResult

if TYPE_CHECKING:
    import numpy as np


class BaseConfusionMatrixResult(BaseResult):
    r"""Implement the base class to implement the confusion matrix
    results.

    Args:
        y_true: The ground truth target labels.
        y_pred: The predicted labels.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.result import BinaryConfusionMatrixResult
    >>> result = BinaryConfusionMatrixResult(
    ...     y_true=np.array([1, 0, 0, 1, 1]), y_pred=np.array([1, 0, 0, 1, 1])
    ... )
    >>> result
    BinaryConfusionMatrixResult(y_true=(5,), y_pred=(5,))
    >>> result.compute_metrics()
    {'confusion_matrix': array([[2, 0], [0, 3]]),
     'count': 5,
     'false_negative_rate': 0.0,
     'false_negative': 0,
     'false_positive_rate': 0.0,
     'false_positive': 0,
     'true_negative_rate': 1.0,
     'true_negative': 2,
     'true_positive_rate': 1.0,
     'true_positive': 3}

    ```
    """

    def __init__(self, y_true: np.ndarray, y_pred: np.ndarray) -> None:
        self._y_true = y_true
        self._y_pred = y_pred

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(y_true={self._y_true.shape}, "
            f"y_pred={self._y_pred.shape})"
        )

    @property
    def y_true(self) -> np.ndarray:
        return self._y_true

    @property
    def y_pred(self) -> np.ndarray:
        return self._y_pred

    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return objects_are_equal(
            self.y_true, other.y_true, equal_nan=equal_nan
        ) and objects_are_equal(self.y_pred, other.y_pred, equal_nan=equal_nan)


class BinaryConfusionMatrixResult(BaseConfusionMatrixResult):
    r"""Implement the confusion matrix result for binary labels.

    Args:
        y_true: The ground truth target labels. This input must
            be an array of shape ``(n_samples, *)`` with ``0`` and
            ``1`` values.
        y_pred: The predicted labels. This input must be an array of
            shape ``(n_samples, *)`` with ``0`` and ``1`` values.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.result import BinaryConfusionMatrixResult
    >>> result = BinaryConfusionMatrixResult(
    ...     y_true=np.array([1, 0, 0, 1, 1]), y_pred=np.array([1, 0, 0, 1, 1])
    ... )
    >>> result
    BinaryConfusionMatrixResult(y_true=(5,), y_pred=(5,))
    >>> result.compute_metrics()
    {'confusion_matrix': array([[2, 0], [0, 3]]),
     'count': 5,
     'false_negative_rate': 0.0,
     'false_negative': 0,
     'false_positive_rate': 0.0,
     'false_positive': 0,
     'true_negative_rate': 1.0,
     'true_negative': 2,
     'true_positive_rate': 1.0,
     'true_positive': 3}

    ```
    """

    def __init__(self, y_true: np.ndarray, y_pred: np.ndarray) -> None:
        check_same_shape_pred(y_true, y_pred)
        super().__init__(y_true=y_true.ravel(), y_pred=y_pred.ravel())

    def compute_metrics(self, prefix: str = "", suffix: str = "") -> dict[str, float]:
        return binary_confusion_matrix_metrics(
            y_true=self._y_true,
            y_pred=self._y_pred,
            prefix=prefix,
            suffix=suffix,
        )

    def generate_figures(
        self, prefix: str = "", suffix: str = ""  # noqa: ARG002
    ) -> dict[str, float]:
        return {}


class MulticlassConfusionMatrixResult(BaseConfusionMatrixResult):
    r"""Implement the confusion matrix result for multiclass labels.

    Args:
        y_true: The ground truth target labels. This input must
            be an array of shape ``(n_samples, *)`` with values in
            ``{0, ..., n_classes-1}``.
        y_pred: The predicted labels. This input must be an array of
            shape ``(n_samples, *)`` with values in
            ``{0, ..., n_classes-1}``.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.result import MulticlassConfusionMatrixResult
    >>> result = MulticlassConfusionMatrixResult(
    ...     y_true=np.array([0, 1, 1, 2, 2, 2]),
    ...     y_pred=np.array([0, 1, 1, 2, 2, 2]),
    ... )
    >>> result
    MulticlassConfusionMatrixResult(y_true=(6,), y_pred=(6,))
    >>> result.compute_metrics()
    {'confusion_matrix': array([[1, 0, 0], [0, 2, 0], [0, 0, 3]]), 'count': 6}

    ```
    """

    def __init__(self, y_true: np.ndarray, y_pred: np.ndarray) -> None:
        check_same_shape_pred(y_true, y_pred)
        super().__init__(y_true=y_true.ravel(), y_pred=y_pred.ravel())

    def compute_metrics(self, prefix: str = "", suffix: str = "") -> dict[str, float]:
        return multiclass_confusion_matrix_metrics(
            y_true=self._y_true,
            y_pred=self._y_pred,
            prefix=prefix,
            suffix=suffix,
        )

    def generate_figures(
        self, prefix: str = "", suffix: str = ""  # noqa: ARG002
    ) -> dict[str, float]:
        return {}


class MultilabelConfusionMatrixResult(BaseConfusionMatrixResult):
    r"""Implement the confusion matrix result for multilabel labels.

    Args:
        y_true: The ground truth target labels. This input must
            be an array of shape ``(n_samples, n_classes)`` with ``0``
            and ``1`` values.
        y_pred: The predicted labels. This input must be an array of
            shape ``(n_samples, n_classes)`` with ``0`` and ``1``
            values.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.result import MultilabelConfusionMatrixResult
    >>> result = MultilabelConfusionMatrixResult(
    ...     y_true=np.array([[1, 0, 1], [0, 1, 0], [0, 1, 0], [1, 0, 1], [1, 0, 1]]),
    ...     y_pred=np.array([[1, 0, 1], [0, 1, 0], [0, 1, 0], [1, 0, 1], [1, 0, 1]]),
    ... )
    >>> result
    MultilabelConfusionMatrixResult(y_true=(5, 3), y_pred=(5, 3))
    >>> result.compute_metrics()
    {'confusion_matrix': array([[[2, 0], [0, 3]],
                                [[3, 0], [0, 2]],
                                [[2, 0], [0, 3]]]),
     'count': 5}

    ```
    """

    def __init__(self, y_true: np.ndarray, y_pred: np.ndarray) -> None:
        check_same_shape_pred(y_true, y_pred)
        super().__init__(y_true=y_true, y_pred=y_pred)

    def compute_metrics(self, prefix: str = "", suffix: str = "") -> dict[str, float]:
        return multilabel_confusion_matrix_metrics(
            y_true=self._y_true,
            y_pred=self._y_pred,
            prefix=prefix,
            suffix=suffix,
        )

    def generate_figures(
        self, prefix: str = "", suffix: str = ""  # noqa: ARG002
    ) -> dict[str, float]:
        return {}
