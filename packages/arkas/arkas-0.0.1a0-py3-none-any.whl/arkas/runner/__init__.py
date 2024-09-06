r"""Contain runners."""

from __future__ import annotations

__all__ = ["BaseRunner", "EvaluationRunner", "is_runner_config", "setup_runner"]

from arkas.runner.base import BaseRunner, is_runner_config, setup_runner
from arkas.runner.evaluation import EvaluationRunner
