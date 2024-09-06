r"""Contain the base class to implement an evaluator."""

from __future__ import annotations

__all__ = ["BaseEvaluator", "BaseLazyEvaluator", "is_evaluator_config", "setup_evaluator"]

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from objectory import AbstractFactory
from objectory.utils import is_object_config

from arkas.result import EmptyResult, Result

if TYPE_CHECKING:
    import polars as pl

    from arkas.result import BaseResult

logger = logging.getLogger(__name__)


class BaseEvaluator(ABC, metaclass=AbstractFactory):
    r"""Define the base class to evaluate a DataFrame.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.evaluator import AccuracyEvaluator
    >>> data = {"pred": np.array([3, 2, 0, 1, 0]), "target": np.array([3, 2, 0, 1, 0])}
    >>> evaluator = AccuracyEvaluator(y_true="target", y_pred="pred")
    >>> evaluator
    AccuracyEvaluator(y_true=target, y_pred=pred)
    >>> result = evaluator.evaluate(data)
    >>> result
    AccuracyResult(y_true=(5,), y_pred=(5,))

    ```
    """

    def evaluate(self, data: dict | pl.DataFrame, lazy: bool = True) -> BaseResult:
        r"""Evaluate the results.

        Args:
            data: The data to evaluate.
            lazy: If ``False``, it forces the computation of the results, otherwise it tries to

        Returns:
            The generated results.

        Example usage:

        ```pycon

        >>> import numpy as np
        >>> from arkas.evaluator import AccuracyEvaluator
        >>> data = {"pred": np.array([3, 2, 0, 1, 0]), "target": np.array([3, 2, 0, 1, 0])}
        >>> evaluator = AccuracyEvaluator(y_true="target", y_pred="pred")
        >>> result = evaluator.evaluate(data)
        >>> result
        AccuracyResult(y_true=(5,), y_pred=(5,))

        ```
        """


class BaseLazyEvaluator(BaseEvaluator):
    r"""Define the base class to evaluate a DataFrame.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.evaluator import AccuracyEvaluator
    >>> data = {"pred": np.array([3, 2, 0, 1, 0]), "target": np.array([3, 2, 0, 1, 0])}
    >>> evaluator = AccuracyEvaluator(y_true="target", y_pred="pred")
    >>> evaluator
    AccuracyEvaluator(y_true=target, y_pred=pred)
    >>> result = evaluator.evaluate(data)
    >>> result
    AccuracyResult(y_true=(5,), y_pred=(5,))

    ```
    """

    def evaluate(self, data: dict | pl.DataFrame, lazy: bool = True) -> BaseResult:
        out = self._evaluate(data)
        if lazy or isinstance(out, EmptyResult):
            return out
        return Result(metrics=out.compute_metrics(), figures=out.generate_figures())

    @abstractmethod
    def _evaluate(self, data: dict | pl.DataFrame) -> BaseResult:
        r"""Evaluate the results.

        Args:
            data: The data to evaluate.

        Returns:
            The generated results.
        """


def is_evaluator_config(config: dict) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``BaseEvaluator``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: The configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration
            for a ``BaseEvaluator`` object.

    Example usage:

    ```pycon

    >>> from arkas.evaluator import is_evaluator_config
    >>> is_evaluator_config({"_target_": "arkas.evaluator.AccuracyEvaluator"})
    True

    ```
    """
    return is_object_config(config, BaseEvaluator)


def setup_evaluator(
    evaluator: BaseEvaluator | dict,
) -> BaseEvaluator:
    r"""Set up an evaluator.

    The evaluator is instantiated from its configuration
    by using the ``BaseEvaluator`` factory function.

    Args:
        evaluator: An evaluator or its configuration.

    Returns:
        An instantiated evaluator.

    Example usage:

    ```pycon

    >>> from arkas.evaluator import setup_evaluator
    >>> evaluator = setup_evaluator(
    ...     {
    ...         "_target_": "arkas.evaluator.AccuracyEvaluator",
    ...         "y_true": "target",
    ...         "y_pred": "pred",
    ...     }
    ... )
    >>> evaluator
    AccuracyEvaluator(y_true=target, y_pred=pred)

    ```
    """
    if isinstance(evaluator, dict):
        logger.info("Initializing an evaluator from its configuration... ")
        evaluator = BaseEvaluator.factory(**evaluator)
    if not isinstance(evaluator, BaseEvaluator):
        logger.warning(f"evaluator is not a `BaseEvaluator` (received: {type(evaluator)})")
    return evaluator
