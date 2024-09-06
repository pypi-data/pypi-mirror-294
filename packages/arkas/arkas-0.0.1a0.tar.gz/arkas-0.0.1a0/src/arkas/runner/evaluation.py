r"""Contain a simple evaluation runner implementation."""

from __future__ import annotations

__all__ = ["EvaluationRunner"]

import logging
from typing import TYPE_CHECKING, Any

from coola.utils import str_indent, str_mapping
from coola.utils.path import sanitize_path
from iden.io import BaseSaver, setup_saver

from arkas.data.ingestor import BaseIngestor, setup_ingestor
from arkas.evaluator import BaseEvaluator, setup_evaluator
from arkas.runner.base import BaseRunner

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


class EvaluationRunner(BaseRunner):
    r"""Implement a simple evaluation runner.

    Args:
        ingestor: The data ingestor or its configuration.
        evaluator: The evaluator or its configuration.
        saver: The metric saver or its configuration.
        path: The path where to save the metrics.

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

    def __init__(
        self,
        ingestor: BaseIngestor | dict,
        evaluator: BaseEvaluator | dict,
        saver: BaseSaver | dict,
        path: Path | str,
    ) -> None:
        self._ingestor = setup_ingestor(ingestor)
        self._evaluator = setup_evaluator(evaluator)
        self._saver = setup_saver(saver)
        self._path = sanitize_path(path)

    def __repr__(self) -> str:
        args = str_indent(
            str_mapping(
                {
                    "ingestor": self._ingestor,
                    "evaluator": self._evaluator,
                    "saver": self._saver,
                    "path": self._path,
                }
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def run(self) -> Any:
        logger.info("Ingesting data...")
        data = self._ingestor.ingest()
        logger.info("Evaluating...")
        result = self._evaluator.evaluate(data)
        logger.info(f"result:\n{result}")
        logger.info("Computing metrics...")
        metrics = result.compute_metrics()
        logger.info(f"Saving metrics at {self._path}...")
        self._saver.save(metrics, path=self._path, exist_ok=True)
