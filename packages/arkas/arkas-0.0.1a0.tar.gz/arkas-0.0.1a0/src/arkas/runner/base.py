r"""Contain the base class to implement a runner."""

from __future__ import annotations

__all__ = ["BaseRunner", "is_runner_config", "setup_runner"]

import logging
from abc import ABC, abstractmethod
from typing import Any

from objectory import AbstractFactory
from objectory.utils import is_object_config

logger = logging.getLogger(__name__)


class BaseRunner(ABC, metaclass=AbstractFactory):
    r"""Define the base class to implement a runner.

    Example usage:

    ```pycon

    >>> import tempfile
    >>> import numpy as np
    >>> from pathlib import Path
    >>> from iden.io import PickleSaver
    >>> from arkas.data.ingestor import Ingestor
    >>> from arkas.evaluator import AccuracyEvaluator
    >>> from arkas.runner import EvaluationRunner
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = Path(tmpdir).joinpath("metrics.pkl")
    ...     runner = EvaluationRunner(
    ...         ingestor=Ingestor(
    ...             data={
    ...                 "pred": np.array([3, 2, 0, 1, 0]),
    ...                 "target": np.array([3, 2, 0, 1, 0]),
    ...             }
    ...         ),
    ...         evaluator=AccuracyEvaluator(y_true="target", y_pred="pred"),
    ...         saver=PickleSaver(),
    ...         path=path,
    ...     )
    ...     print(runner)
    ...     runner.run()
    ...
    EvaluationRunner(
      (ingestor): Ingestor(num_items=2)
      (evaluator): AccuracyEvaluator(y_true=target, y_pred=pred)
      (saver): PickleSaver(protocol=5)
      (path): .../metrics.pkl
    )

    ```
    """

    @abstractmethod
    def run(self) -> Any:
        r"""Execute the logic of the runner.

        Returns:
            Any artifact of the runner

        Example usage:

        ```pycon

        >>> import tempfile
        >>> import numpy as np
        >>> from pathlib import Path
        >>> from iden.io import PickleSaver
        >>> from arkas.data.ingestor import Ingestor
        >>> from arkas.evaluator import AccuracyEvaluator
        >>> from arkas.runner import EvaluationRunner
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     path = Path(tmpdir).joinpath("metrics.pkl")
        ...     runner = EvaluationRunner(
        ...         ingestor=Ingestor(
        ...             data={
        ...                 "pred": np.array([3, 2, 0, 1, 0]),
        ...                 "target": np.array([3, 2, 0, 1, 0]),
        ...             }
        ...         ),
        ...         evaluator=AccuracyEvaluator(y_true="target", y_pred="pred"),
        ...         saver=PickleSaver(),
        ...         path=path,
        ...     )
        ...     runner.run()
        ...

        ```
        """


def is_runner_config(config: dict) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``BaseRunner``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: The configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration
            for a ``BaseRunner`` object.

    Example usage:

    ```pycon

    >>> from arkas.runner import is_runner_config
    >>> is_runner_config({"_target_": "arkas.runner.EvaluationRunner"})
    True

    ```
    """
    return is_object_config(config, BaseRunner)


def setup_runner(
    runner: BaseRunner | dict,
) -> BaseRunner:
    r"""Set up a runner.

    The runner is instantiated from its configuration
    by using the ``BaseRunner`` factory function.

    Args:
        runner: Specifies a runner or its configuration.

    Returns:
        An instantiated runner.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from arkas.runner import setup_runner
    >>> runner = setup_runner(
    ...     {
    ...         "_target_": "arkas.runner.EvaluationRunner",
    ...         "ingestor": {
    ...             "_target_": "arkas.data.ingestor.Ingestor",
    ...             "data": {
    ...                 "pred": np.array([3, 2, 0, 1, 0]),
    ...                 "target": np.array([3, 2, 0, 1, 0]),
    ...             },
    ...         },
    ...         "evaluator": {
    ...             "_target_": "arkas.evaluator.AccuracyEvaluator",
    ...             "y_true": "target",
    ...             "y_pred": "pred",
    ...         },
    ...         "saver": {"_target_": "iden.io.PickleSaver"},
    ...         "path": "/tmp/data/metrics.pkl",
    ...     }
    ... )
    >>> runner
    EvaluationRunner(
      (ingestor): Ingestor(num_items=2)
      (evaluator): AccuracyEvaluator(y_true=target, y_pred=pred)
      (saver): PickleSaver(protocol=5)
      (path): .../metrics.pkl
    )

    ```
    """
    if isinstance(runner, dict):
        logger.info("Initializing a runner from its configuration... ")
        runner = BaseRunner.factory(**runner)
    if not isinstance(runner, BaseRunner):
        logger.warning(f"runner is not a `BaseRunner` (received: {type(runner)})")
    return runner
