r"""Implement the F-beta result."""

from __future__ import annotations

__all__ = [
    "BaseFbetaResult",
    "BinaryFbetaResult",
    "MulticlassFbetaResult",
    "MultilabelFbetaResult",
]

from typing import TYPE_CHECKING, Any

from coola import objects_are_equal

from arkas.metric.fbeta import (
    binary_fbeta_metrics,
    multiclass_fbeta_metrics,
    multilabel_fbeta_metrics,
)
from arkas.metric.utils import check_same_shape_pred
from arkas.result.base import BaseResult

if TYPE_CHECKING:
    from collections.abc import Sequence

    import numpy as np


class BaseFbetaResult(BaseResult):
    r"""Implement the base class to implement the F-beta results.

    Args:
        y_true: The ground truth target labels.
        y_pred: The predicted labels.
        betas: The betas used to compute the F-beta scores.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.result import BinaryFbetaResult
    >>> result = BinaryFbetaResult(
    ...     y_true=np.array([1, 0, 0, 1, 1]), y_pred=np.array([1, 0, 0, 1, 1])
    ... )
    >>> result
    BinaryFbetaResult(y_true=(5,), y_pred=(5,), betas=(1,))
    >>> result.compute_metrics()
    {'count': 5, 'f1': 1.0}

    ```
    """

    def __init__(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        betas: Sequence[float] = (1,),
    ) -> None:
        self._y_true = y_true
        self._y_pred = y_pred
        self._betas = tuple(betas)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(y_true={self._y_true.shape}, "
            f"y_pred={self._y_pred.shape}, betas={self._betas})"
        )

    @property
    def betas(self) -> tuple[float, ...]:
        return self._betas

    @property
    def y_true(self) -> np.ndarray:
        return self._y_true

    @property
    def y_pred(self) -> np.ndarray:
        return self._y_pred

    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return (
            objects_are_equal(self.y_true, other.y_true, equal_nan=equal_nan)
            and objects_are_equal(self.y_pred, other.y_pred, equal_nan=equal_nan)
            and objects_are_equal(self.betas, other.betas, equal_nan=equal_nan)
        )


class BinaryFbetaResult(BaseFbetaResult):
    r"""Implement the F-beta result for binary labels.

    Args:
        y_true: The ground truth target labels. This input must
            be an array of shape ``(n_samples, *)`` with ``0`` and
            ``1`` values.
        y_pred: The predicted labels. This input must be an array of
            shape ``(n_samples, *)`` with ``0`` and ``1`` values.
        betas: The betas used to compute the F-beta scores.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.result import BinaryFbetaResult
    >>> result = BinaryFbetaResult(
    ...     y_true=np.array([1, 0, 0, 1, 1]), y_pred=np.array([1, 0, 0, 1, 1])
    ... )
    >>> result
    BinaryFbetaResult(y_true=(5,), y_pred=(5,), betas=(1,))
    >>> result.compute_metrics()
    {'count': 5, 'f1': 1.0}

    ```
    """

    def __init__(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        betas: Sequence[float] = (1,),
    ) -> None:
        check_same_shape_pred(y_true, y_pred)
        super().__init__(y_true=y_true.ravel(), y_pred=y_pred.ravel(), betas=betas)

    def compute_metrics(self, prefix: str = "", suffix: str = "") -> dict[str, float]:
        return binary_fbeta_metrics(
            y_true=self._y_true,
            y_pred=self._y_pred,
            prefix=prefix,
            suffix=suffix,
            betas=self._betas,
        )

    def generate_figures(
        self, prefix: str = "", suffix: str = ""  # noqa: ARG002
    ) -> dict[str, float]:
        return {}


class MulticlassFbetaResult(BaseFbetaResult):
    r"""Implement the F-beta result for multiclass labels.

    Args:
        y_true: The ground truth target labels. This input must
            be an array of shape ``(n_samples, *)`` with values in
            ``{0, ..., n_classes-1}``.
        y_pred: The predicted labels. This input must be an array of
            shape ``(n_samples, *)`` with values in
            ``{0, ..., n_classes-1}``.
        betas: The betas used to compute the F-beta scores.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.result import MulticlassFbetaResult
    >>> result = MulticlassFbetaResult(
    ...     y_true=np.array([0, 0, 1, 1, 2, 2]),
    ...     y_pred=np.array([0, 0, 1, 1, 2, 2]),
    ... )
    >>> result
    MulticlassFbetaResult(y_true=(6,), y_pred=(6,), betas=(1,))
    >>> result.compute_metrics()
    {'count': 6,
     'f1': array([1., 1., 1.]),
     'macro_f1': 1.0,
     'micro_f1': 1.0,
     'weighted_f1': 1.0}

    ```
    """

    def __init__(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        betas: Sequence[float] = (1,),
    ) -> None:
        check_same_shape_pred(y_true, y_pred)
        super().__init__(y_true=y_true.ravel(), y_pred=y_pred.ravel(), betas=betas)

    def compute_metrics(self, prefix: str = "", suffix: str = "") -> dict[str, float]:
        return multiclass_fbeta_metrics(
            y_true=self._y_true,
            y_pred=self._y_pred,
            prefix=prefix,
            suffix=suffix,
            betas=self._betas,
        )

    def generate_figures(
        self, prefix: str = "", suffix: str = ""  # noqa: ARG002
    ) -> dict[str, float]:
        return {}


class MultilabelFbetaResult(BaseFbetaResult):
    r"""Implement the F-beta result for multilabel labels.

    Args:
        y_true: The ground truth target labels. This input must
            be an array of shape ``(n_samples, n_classes)`` with ``0``
            and ``1`` values.
        y_pred: The predicted labels. This input must be an array of
            shape ``(n_samples, n_classes)`` with ``0`` and ``1``
            values.
        betas: The betas used to compute the F-beta scores.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.result import MultilabelFbetaResult
    >>> result = MultilabelFbetaResult(
    ...     y_true=np.array([[1, 0, 1], [0, 1, 0], [0, 1, 0], [1, 0, 1], [1, 0, 1]]),
    ...     y_pred=np.array([[1, 0, 1], [0, 1, 0], [0, 1, 0], [1, 0, 1], [1, 0, 1]]),
    ... )
    >>> result
    MultilabelFbetaResult(y_true=(5, 3), y_pred=(5, 3), betas=(1,))
    >>> result.compute_metrics()
    {'count': 5,
     'f1': array([1., 1., 1.]),
     'macro_f1': 1.0,
     'micro_f1': 1.0,
     'weighted_f1': 1.0}

    ```
    """

    def __init__(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        betas: Sequence[float] = (1,),
    ) -> None:
        check_same_shape_pred(y_true, y_pred)
        super().__init__(y_true=y_true, y_pred=y_pred, betas=betas)

    def compute_metrics(self, prefix: str = "", suffix: str = "") -> dict[str, float]:
        return multilabel_fbeta_metrics(
            y_true=self._y_true,
            y_pred=self._y_pred,
            prefix=prefix,
            suffix=suffix,
            betas=self._betas,
        )

    def generate_figures(
        self, prefix: str = "", suffix: str = ""  # noqa: ARG002
    ) -> dict[str, float]:
        return {}
