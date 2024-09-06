r"""Implement the F-beta metrics."""

from __future__ import annotations

__all__ = [
    "binary_fbeta_metrics",
    "fbeta_metrics",
    "multiclass_fbeta_metrics",
    "multilabel_fbeta_metrics",
]

from typing import TYPE_CHECKING

import numpy as np
from sklearn import metrics

from arkas.metric.precision import find_label_type
from arkas.metric.utils import (
    check_label_type,
    preprocess_pred,
    preprocess_pred_multilabel,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence


def fbeta_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    betas: Sequence[float] = (1,),
    label_type: str = "auto",
    prefix: str = "",
    suffix: str = "",
) -> dict[str, float | np.ndarray]:
    r"""Return the fbeta metrics.

    Args:
        y_true: The ground truth target labels. This input must
            be an array of shape ``(n_samples,)`` or
            ``(n_samples, n_classes)``.
        y_pred: The predicted labels. This input must be an array of
            shape ``(n_samples,)`` or ``(n_samples, n_classes)``.
        betas: The betas used to compute the F-beta scores.
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
    >>> from arkas.metric import fbeta_metrics
    >>> # auto
    >>> fbeta_metrics(y_true=np.array([1, 0, 0, 1, 1]), y_pred=np.array([1, 0, 0, 1, 1]))
    {'count': 5, 'f1': 1.0}
    >>> # binary
    >>> fbeta_metrics(
    ...     y_true=np.array([1, 0, 0, 1, 1]),
    ...     y_pred=np.array([1, 0, 0, 1, 1]),
    ...     label_type="binary",
    ... )
    {'count': 5, 'f1': 1.0}
    >>> # multiclass
    >>> fbeta_metrics(
    ...     y_true=np.array([0, 0, 1, 1, 2, 2]),
    ...     y_pred=np.array([0, 0, 1, 1, 2, 2]),
    ...     label_type="multiclass",
    ... )
    {'count': 6,
     'f1': array([1., 1., 1.]),
     'macro_f1': 1.0,
     'micro_f1': 1.0,
     'weighted_f1': 1.0}
    >>> # multilabel
    >>> fbeta_metrics(
    ...     y_true=np.array([[1, 0, 1], [0, 1, 0], [0, 1, 0], [1, 0, 1], [1, 0, 1]]),
    ...     y_pred=np.array([[1, 0, 1], [0, 1, 0], [0, 1, 0], [1, 0, 1], [1, 0, 1]]),
    ...     label_type="multilabel",
    ... )
    {'count': 5,
     'f1': array([1., 1., 1.]),
     'macro_f1': 1.0,
     'micro_f1': 1.0,
     'weighted_f1': 1.0}

    ```
    """
    check_label_type(label_type)
    if label_type == "auto":
        label_type = find_label_type(y_true=y_true, y_pred=y_pred)
    if label_type == "binary":
        return binary_fbeta_metrics(
            y_true=y_true.ravel(),
            y_pred=y_pred.ravel(),
            betas=betas,
            prefix=prefix,
            suffix=suffix,
        )
    if label_type == "multilabel":
        return multilabel_fbeta_metrics(
            y_true=y_true,
            y_pred=y_pred,
            betas=betas,
            prefix=prefix,
            suffix=suffix,
        )
    return multiclass_fbeta_metrics(
        y_true=y_true.ravel(),
        y_pred=y_pred.ravel(),
        betas=betas,
        prefix=prefix,
        suffix=suffix,
    )


def binary_fbeta_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    betas: Sequence[float] = (1,),
    prefix: str = "",
    suffix: str = "",
) -> dict[str, float]:
    r"""Return the F-beta metrics for binary labels.

    Args:
        y_true: The ground truth target labels. This input must
            be an array of shape ``(n_samples,)``.
        y_pred: The predicted labels. This input must
            be an array of shape ``(n_samples,)``.
        betas: The betas used to compute the F-beta scores.
        prefix: The key prefix in the returned dictionary.
        suffix: The key suffix in the returned dictionary.

    Returns:
        The computed metrics.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.metric import binary_fbeta_metrics
    >>> binary_fbeta_metrics(
    ...     y_true=np.array([1, 0, 0, 1, 1]),
    ...     y_pred=np.array([1, 0, 0, 1, 1]),
    ... )
    {'count': 5, 'f1': 1.0}

    ```
    """
    return _eval_all(
        fn=_binary_fbeta_metrics,
        y_true=y_true.ravel(),
        y_pred=y_pred.ravel(),
        betas=betas,
        prefix=prefix,
        suffix=suffix,
    )


def multiclass_fbeta_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    betas: Sequence[float] = (1,),
    prefix: str = "",
    suffix: str = "",
) -> dict[str, float]:
    r"""Return the F-beta metrics for multiclass labels.

    Args:
        y_true: The ground truth target labels. This input must
            be an array of shape ``(n_samples,)``.
        y_pred: The predicted labels. This input must
            be an array of shape ``(n_samples,)``.
        betas: The betas used to compute the F-beta scores.
        prefix: The key prefix in the returned dictionary.
        suffix: The key suffix in the returned dictionary.

    Returns:
        The computed metrics.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.metric import multiclass_fbeta_metrics
    >>> multiclass_fbeta_metrics(
    ...     y_true=np.array([0, 0, 1, 1, 2, 2]),
    ...     y_pred=np.array([0, 0, 1, 1, 2, 2]),
    ... )
    {'count': 6,
     'f1': array([1., 1., 1.]),
     'macro_f1': 1.0,
     'micro_f1': 1.0,
     'weighted_f1': 1.0}

    ```
    """
    return _eval_all(
        fn=_multiclass_fbeta_metrics,
        y_true=y_true.ravel(),
        y_pred=y_pred.ravel(),
        betas=betas,
        prefix=prefix,
        suffix=suffix,
    )


def multilabel_fbeta_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    betas: Sequence[float] = (1,),
    prefix: str = "",
    suffix: str = "",
) -> dict[str, float]:
    r"""Return the F-beta metrics for multilabel labels.

    Args:
        y_true: The ground truth target labels. This input must
            be an array of shape ``(n_samples,)``.
        y_pred: The predicted labels. This input must
            be an array of shape ``(n_samples,)``.
        betas: The betas used to compute the F-beta scores.
        prefix: The key prefix in the returned dictionary.
        suffix: The key suffix in the returned dictionary.

    Returns:
        The computed metrics.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.metric import multilabel_fbeta_metrics
    >>> multilabel_fbeta_metrics(
    ...     y_true=np.array([[1, 0, 1], [0, 1, 0], [0, 1, 0], [1, 0, 1], [1, 0, 1]]),
    ...     y_pred=np.array([[1, 0, 1], [0, 1, 0], [0, 1, 0], [1, 0, 1], [1, 0, 1]]),
    ... )
    {'count': 5,
     'f1': array([1., 1., 1.]),
     'macro_f1': 1.0,
     'micro_f1': 1.0,
     'weighted_f1': 1.0}

    ```
    """
    return _eval_all(
        fn=_multilabel_fbeta_metrics,
        y_true=y_true,
        y_pred=y_pred,
        betas=betas,
        prefix=prefix,
        suffix=suffix,
    )


def _binary_fbeta_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    beta: float = 1,
    prefix: str = "",
    suffix: str = "",
) -> dict[str, float]:
    r"""Return the F-beta metrics for binary labels.

    Args:
        y_true: The ground truth target labels. This input must
            be an array of shape ``(n_samples,)``.
        y_pred: The predicted labels. This input must
            be an array of shape ``(n_samples,)``.
        beta: The beta used to compute the F-beta score.
        prefix: The key prefix in the returned dictionary.
        suffix: The key suffix in the returned dictionary.

    Returns:
        The computed metrics.
    """
    y_true, y_pred = preprocess_pred(y_true=y_true, y_pred=y_pred, nan="remove")

    count, fbeta = y_true.size, float("nan")
    if count > 0:
        fbeta = float(metrics.fbeta_score(y_true=y_true, y_pred=y_pred, beta=beta))
    return {f"{prefix}count{suffix}": count, f"{prefix}f{beta}{suffix}": fbeta}


def _multiclass_fbeta_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    beta: float = 1,
    prefix: str = "",
    suffix: str = "",
) -> dict[str, float | np.ndarray]:
    r"""Return the F-beta metrics for multiclass labels.

    Args:
        y_true: The ground truth target labels. This input must
            be an array of shape ``(n_samples,)``.
        y_pred: The predicted labels. This input must
            be an array of shape ``(n_samples,)``.
        beta: The beta used to compute the F-beta score.
        prefix: The key prefix in the returned dictionary.
        suffix: The key suffix in the returned dictionary.

    Returns:
        The computed metrics.
    """
    y_true, y_pred = preprocess_pred(y_true=y_true, y_pred=y_pred, nan="remove")

    n_samples = y_true.shape[0]
    macro_fbeta, micro_fbeta, weighted_fbeta = float("nan"), float("nan"), float("nan")
    n_classes = y_pred.shape[1] if y_pred.ndim == 2 else 0 if n_samples == 0 else 1
    fbeta = np.full((n_classes,), fill_value=float("nan"))
    if n_samples > 0:
        macro_fbeta = float(
            metrics.fbeta_score(
                y_true=y_true, y_pred=y_pred, beta=beta, average="macro", zero_division=0.0
            )
        )
        micro_fbeta = float(
            metrics.fbeta_score(
                y_true=y_true, y_pred=y_pred, beta=beta, average="micro", zero_division=0.0
            )
        )
        weighted_fbeta = float(
            metrics.fbeta_score(
                y_true=y_true, y_pred=y_pred, beta=beta, average="weighted", zero_division=0.0
            )
        )
        fbeta = np.asarray(
            metrics.fbeta_score(
                y_true=y_true, y_pred=y_pred, beta=beta, average=None, zero_division=0.0
            )
        ).ravel()
    return {
        f"{prefix}count{suffix}": n_samples,
        f"{prefix}f{beta}{suffix}": fbeta,
        f"{prefix}macro_f{beta}{suffix}": macro_fbeta,
        f"{prefix}micro_f{beta}{suffix}": micro_fbeta,
        f"{prefix}weighted_f{beta}{suffix}": weighted_fbeta,
    }


def _multilabel_fbeta_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    beta: float = 1,
    prefix: str = "",
    suffix: str = "",
) -> dict[str, float | np.ndarray]:
    r"""Return the fbeta metrics for multilabel labels.

    Args:
        y_true: The ground truth target labels. This input must
            be an array of shape ``(n_samples, n_classes)``.
        y_pred: The predicted labels. This input must
            be an array of shape ``(n_samples, n_classes)``.
        beta: The beta used to compute the F-beta score.
        prefix: The key prefix in the returned dictionary.
        suffix: The key suffix in the returned dictionary.

    Returns:
        The computed metrics.
    """
    y_true, y_pred = preprocess_pred_multilabel(y_true, y_pred, nan="remove")

    fbeta = np.array([])
    macro_fbeta, micro_fbeta, weighted_fbeta = float("nan"), float("nan"), float("nan")
    n_samples = y_true.shape[0]
    if n_samples > 0:
        fbeta = np.array(
            metrics.fbeta_score(
                y_true=y_true,
                y_pred=y_pred,
                beta=beta,
                average="binary" if y_pred.shape[1] == 1 else None,
            )
        ).ravel()
        macro_fbeta = float(
            metrics.fbeta_score(y_true=y_true, y_pred=y_pred, beta=beta, average="macro")
        )
        micro_fbeta = float(
            metrics.fbeta_score(y_true=y_true, y_pred=y_pred, beta=beta, average="micro")
        )
        weighted_fbeta = float(
            metrics.fbeta_score(y_true=y_true, y_pred=y_pred, beta=beta, average="weighted")
        )
    return {
        f"{prefix}count{suffix}": n_samples,
        f"{prefix}f{beta}{suffix}": fbeta,
        f"{prefix}macro_f{beta}{suffix}": macro_fbeta,
        f"{prefix}micro_f{beta}{suffix}": micro_fbeta,
        f"{prefix}weighted_f{beta}{suffix}": weighted_fbeta,
    }


def _eval_all(
    fn: Callable,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    betas: Sequence[float],
    *,
    prefix: str = "",
    suffix: str = "",
) -> dict[str, float | np.ndarray]:
    r"""Evaluate the function for all the betas and merge the results in
    a single dictionary.

    Args:
        fn: The function to evaluate.
        y_true: The ground truth target labels. This input must
            be an array of shape ``(n_samples,)`` or
            ``(n_samples, n_classes)``.
        y_pred: The predicted labels. This input must be an array of
            shape ``(n_samples,)`` or ``(n_samples, n_classes)``.
        betas: The betas used to compute the F-beta scores.
        prefix: The key prefix in the returned dictionary.
        suffix: The key suffix in the returned dictionary.

    Returns:
        The computed metrics.
    """
    out = {}
    for beta in betas:
        out |= fn(y_true=y_true, y_pred=y_pred, beta=beta, prefix=prefix, suffix=suffix)
    return out
