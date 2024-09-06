r"""Implement accuracy metrics."""

from __future__ import annotations

__all__ = ["accuracy_metrics", "balanced_accuracy_metrics"]


from typing import TYPE_CHECKING

from sklearn import metrics

from arkas.metric.utils import preprocess_pred

if TYPE_CHECKING:
    import numpy as np


def accuracy_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    prefix: str = "",
    suffix: str = "",
) -> dict[str, float]:
    r"""Return the accuracy metrics.

    Args:
        y_true: The ground truth target labels.
        y_pred: The predicted labels.
        prefix: The key prefix in the returned dictionary.
        suffix: The key suffix in the returned dictionary.

    Returns:
        The computed metrics.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.metric import accuracy_metrics
    >>> accuracy_metrics(y_true=np.array([1, 0, 0, 1, 1]), y_pred=np.array([1, 0, 0, 1, 1]))
    {'accuracy': 1.0, 'count_correct': 5, 'count_incorrect': 0, 'count': 5, 'error': 0.0}

    ```
    """
    y_true, y_pred = preprocess_pred(y_true=y_true.ravel(), y_pred=y_pred.ravel(), nan="remove")

    count = y_true.size
    count_correct = int(metrics.accuracy_score(y_true=y_true, y_pred=y_pred, normalize=False))
    accuracy = float(count_correct / count) if count > 0 else float("nan")
    return {
        f"{prefix}accuracy{suffix}": accuracy,
        f"{prefix}count_correct{suffix}": count_correct,
        f"{prefix}count_incorrect{suffix}": count - count_correct,
        f"{prefix}count{suffix}": count,
        f"{prefix}error{suffix}": 1.0 - accuracy,
    }


def balanced_accuracy_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    prefix: str = "",
    suffix: str = "",
) -> dict[str, float]:
    r"""Return the accuracy metrics.

    Args:
        y_true: The ground truth target labels.
        y_pred: The predicted labels.
        prefix: The key prefix in the returned dictionary.
        suffix: The key suffix in the returned dictionary.

    Returns:
        The computed metrics.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.metric import balanced_accuracy_metrics
    >>> balanced_accuracy_metrics(
    ...     y_true=np.array([1, 0, 0, 1, 1]), y_pred=np.array([1, 0, 0, 1, 1])
    ... )
    {'balanced_accuracy': 1.0, 'count': 5}

    ```
    """
    y_true, y_pred = preprocess_pred(y_true=y_true.ravel(), y_pred=y_pred.ravel(), nan="remove")

    count = y_true.size
    accuracy = float("nan")
    if count > 0:
        accuracy = float(metrics.balanced_accuracy_score(y_true=y_true, y_pred=y_pred))
    return {f"{prefix}balanced_accuracy{suffix}": accuracy, f"{prefix}count{suffix}": count}
