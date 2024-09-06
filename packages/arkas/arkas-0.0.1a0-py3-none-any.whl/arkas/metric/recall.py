r"""Implement the recall result."""

from __future__ import annotations

__all__ = [
    "binary_recall_metrics",
    "multiclass_recall_metrics",
    "multilabel_recall_metrics",
    "recall_metrics",
]


import numpy as np
from sklearn import metrics

from arkas.metric.precision import find_label_type
from arkas.metric.utils import (
    check_label_type,
    preprocess_pred,
    preprocess_pred_multilabel,
)


def recall_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    label_type: str = "auto",
    prefix: str = "",
    suffix: str = "",
) -> dict[str, float | np.ndarray]:
    r"""Return the recall metrics.

    Args:
        y_true: The ground truth target labels. This input must
            be an array of shape ``(n_samples,)`` or
            ``(n_samples, n_classes)``.
        y_pred: The predicted labels. This input must be an array of
            shape ``(n_samples,)`` or ``(n_samples, n_classes)``.
        label_type: The type of labels used to evaluate the metrics.
            The valid values are: ``'binary'``, ``'multiclass'``,
            and ``'multilabel'``. If ``'binary'`` or ``'multilabel'``,
            ``y_true`` values  must be ``0`` and ``1``.
        prefix: The key prefix in the returned dictionary.
        suffix: The key suffix in the returned dictionary.

    Returns:
        The computed metrics.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.metric import recall_metrics
    >>> # auto
    >>> recall_metrics(y_true=np.array([1, 0, 0, 1, 1]), y_pred=np.array([1, 0, 0, 1, 1]))
    {'count': 5, 'recall': 1.0}
    >>> # binary
    >>> recall_metrics(
    ...     y_true=np.array([1, 0, 0, 1, 1]),
    ...     y_pred=np.array([1, 0, 0, 1, 1]),
    ...     label_type="binary",
    ... )
    {'count': 5, 'recall': 1.0}
    >>> # multiclass
    >>> recall_metrics(
    ...     y_true=np.array([0, 0, 1, 1, 2, 2]),
    ...     y_pred=np.array([0, 0, 1, 1, 2, 2]),
    ...     label_type="multiclass",
    ... )
    {'count': 6,
     'macro_recall': 1.0,
     'micro_recall': 1.0,
     'recall': array([1., 1., 1.]),
     'weighted_recall': 1.0}
    >>> # multilabel
    >>> recall_metrics(
    ...     y_true=np.array([[1, 0, 1], [0, 1, 0], [0, 1, 0], [1, 0, 1], [1, 0, 1]]),
    ...     y_pred=np.array([[1, 0, 1], [0, 1, 0], [0, 1, 0], [1, 0, 1], [1, 0, 1]]),
    ...     label_type="multilabel",
    ... )
    {'count': 5,
     'macro_recall': 1.0,
     'micro_recall': 1.0,
     'recall': array([1., 1., 1.]),
     'weighted_recall': 1.0}

    ```
    """
    check_label_type(label_type)
    if label_type == "auto":
        label_type = find_label_type(y_true=y_true, y_pred=y_pred)
    if label_type == "binary":
        return binary_recall_metrics(y_true=y_true, y_pred=y_pred, prefix=prefix, suffix=suffix)
    if label_type == "multilabel":
        return multilabel_recall_metrics(y_true=y_true, y_pred=y_pred, prefix=prefix, suffix=suffix)
    return multiclass_recall_metrics(y_true=y_true, y_pred=y_pred, prefix=prefix, suffix=suffix)


def binary_recall_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    prefix: str = "",
    suffix: str = "",
) -> dict[str, float]:
    r"""Return the recall metrics for binary labels.

    Args:
        y_true: The ground truth target labels. This input must
            be an array of shape ``(n_samples,)``.
        y_pred: The predicted labels. This input must
            be an array of shape ``(n_samples,)``.
        prefix: The key prefix in the returned dictionary.
        suffix: The key suffix in the returned dictionary.

    Returns:
        The computed metrics.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.metric import binary_recall_metrics
    >>> binary_recall_metrics(
    ...     y_true=np.array([1, 0, 0, 1, 1]), y_pred=np.array([1, 0, 0, 1, 1])
    ... )
    {'count': 5, 'recall': 1.0}

    ```
    """
    y_true, y_pred = preprocess_pred(y_true=y_true.ravel(), y_pred=y_pred.ravel(), nan="remove")

    count, recall = y_true.size, float("nan")
    if count > 0:
        recall = float(metrics.recall_score(y_true=y_true, y_pred=y_pred))
    return {f"{prefix}count{suffix}": count, f"{prefix}recall{suffix}": recall}


def multiclass_recall_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    prefix: str = "",
    suffix: str = "",
) -> dict[str, float | np.ndarray]:
    r"""Return the recall metrics for multiclass labels.

    Args:
        y_true: The ground truth target labels. This input must
            be an array of shape ``(n_samples,)``.
        y_pred: The predicted labels. This input must
            be an array of shape ``(n_samples,)``.
        prefix: The key prefix in the returned dictionary.
        suffix: The key suffix in the returned dictionary.

    Returns:
        The computed metrics.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.metric import multiclass_recall_metrics
    >>> multiclass_recall_metrics(
    ...     y_true=np.array([0, 0, 1, 1, 2, 2]), y_pred=np.array([0, 0, 1, 1, 2, 2])
    ... )
    {'count': 6,
     'macro_recall': 1.0,
     'micro_recall': 1.0,
     'recall': array([1., 1., 1.]),
     'weighted_recall': 1.0}

    ```
    """
    y_true, y_pred = preprocess_pred(y_true=y_true.ravel(), y_pred=y_pred.ravel(), nan="remove")

    n_samples = y_true.shape[0]
    macro_recall, micro_recall, weighted_recall = float("nan"), float("nan"), float("nan")
    n_classes = y_pred.shape[1] if y_pred.ndim == 2 else 0 if n_samples == 0 else 1
    recall = np.full((n_classes,), fill_value=float("nan"))
    if n_samples > 0:
        macro_recall = float(
            metrics.recall_score(y_true=y_true, y_pred=y_pred, average="macro", zero_division=0.0)
        )
        micro_recall = float(
            metrics.recall_score(y_true=y_true, y_pred=y_pred, average="micro", zero_division=0.0)
        )
        weighted_recall = float(
            metrics.recall_score(
                y_true=y_true, y_pred=y_pred, average="weighted", zero_division=0.0
            )
        )
        recall = np.asarray(
            metrics.recall_score(y_true=y_true, y_pred=y_pred, average=None, zero_division=0.0)
        ).ravel()
    return {
        f"{prefix}count{suffix}": n_samples,
        f"{prefix}macro_recall{suffix}": macro_recall,
        f"{prefix}micro_recall{suffix}": micro_recall,
        f"{prefix}recall{suffix}": recall,
        f"{prefix}weighted_recall{suffix}": weighted_recall,
    }


def multilabel_recall_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    prefix: str = "",
    suffix: str = "",
) -> dict[str, float | np.ndarray]:
    r"""Return the recall metrics for multilabel labels.

    Args:
        y_true: The ground truth target labels. This input must
            be an array of shape ``(n_samples, n_classes)``.
        y_pred: The predicted labels. This input must
            be an array of shape ``(n_samples, n_classes)``.
        prefix: The key prefix in the returned dictionary.
        suffix: The key suffix in the returned dictionary.

    Returns:
        The computed metrics.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.metric import multilabel_recall_metrics
    >>> multilabel_recall_metrics(
    ...     y_true=np.array([[1, 0, 1], [0, 1, 0], [0, 1, 0], [1, 0, 1], [1, 0, 1]]),
    ...     y_pred=np.array([[1, 0, 1], [0, 1, 0], [0, 1, 0], [1, 0, 1], [1, 0, 1]]),
    ... )
    {'count': 5,
     'macro_recall': 1.0,
     'micro_recall': 1.0,
     'recall': array([1., 1., 1.]),
     'weighted_recall': 1.0}

    ```
    """
    y_true, y_pred = preprocess_pred_multilabel(y_true, y_pred, nan="remove")

    recall = np.array([])
    macro_recall, micro_recall, weighted_recall = float("nan"), float("nan"), float("nan")
    n_samples = y_true.shape[0]
    if n_samples > 0:
        recall = np.array(
            metrics.recall_score(
                y_true=y_true,
                y_pred=y_pred,
                average="binary" if y_pred.shape[1] == 1 else None,
            )
        ).ravel()
        macro_recall = float(metrics.recall_score(y_true=y_true, y_pred=y_pred, average="macro"))
        micro_recall = float(metrics.recall_score(y_true=y_true, y_pred=y_pred, average="micro"))
        weighted_recall = float(
            metrics.recall_score(y_true=y_true, y_pred=y_pred, average="weighted")
        )
    return {
        f"{prefix}count{suffix}": n_samples,
        f"{prefix}macro_recall{suffix}": macro_recall,
        f"{prefix}micro_recall{suffix}": micro_recall,
        f"{prefix}recall{suffix}": recall,
        f"{prefix}weighted_recall{suffix}": weighted_recall,
    }
