r"""Contain results."""

from __future__ import annotations

__all__ = [
    "AccuracyResult",
    "AveragePrecisionResult",
    "BalancedAccuracyResult",
    "BaseResult",
    "BinaryAveragePrecisionResult",
    "BinaryClassificationResult",
    "BinaryConfusionMatrixResult",
    "BinaryFbetaResult",
    "BinaryJaccardResult",
    "BinaryPrecisionResult",
    "BinaryRecallResult",
    "BinaryRocAucResult",
    "EmptyResult",
    "MappingResult",
    "MulticlassAveragePrecisionResult",
    "MulticlassConfusionMatrixResult",
    "MulticlassFbetaResult",
    "MulticlassJaccardResult",
    "MulticlassPrecisionResult",
    "MulticlassRecallResult",
    "MulticlassRocAucResult",
    "MultilabelAveragePrecisionResult",
    "MultilabelConfusionMatrixResult",
    "MultilabelFbetaResult",
    "MultilabelJaccardResult",
    "MultilabelPrecisionResult",
    "MultilabelRecallResult",
    "MultilabelRocAucResult",
    "PrecisionResult",
    "RecallResult",
    "Result",
    "SequentialResult",
]

from arkas.result.accuracy import AccuracyResult, BalancedAccuracyResult
from arkas.result.ap import (
    AveragePrecisionResult,
    BinaryAveragePrecisionResult,
    MulticlassAveragePrecisionResult,
    MultilabelAveragePrecisionResult,
)
from arkas.result.base import BaseResult
from arkas.result.binary_classification import BinaryClassificationResult
from arkas.result.confmat import (
    BinaryConfusionMatrixResult,
    MulticlassConfusionMatrixResult,
    MultilabelConfusionMatrixResult,
)
from arkas.result.fbeta import (
    BinaryFbetaResult,
    MulticlassFbetaResult,
    MultilabelFbetaResult,
)
from arkas.result.jaccard import (
    BinaryJaccardResult,
    MulticlassJaccardResult,
    MultilabelJaccardResult,
)
from arkas.result.mapping import MappingResult
from arkas.result.precision import (
    BinaryPrecisionResult,
    MulticlassPrecisionResult,
    MultilabelPrecisionResult,
    PrecisionResult,
)
from arkas.result.recall import (
    BinaryRecallResult,
    MulticlassRecallResult,
    MultilabelRecallResult,
    RecallResult,
)
from arkas.result.roc_auc import (
    BinaryRocAucResult,
    MulticlassRocAucResult,
    MultilabelRocAucResult,
)
from arkas.result.sequential import SequentialResult
from arkas.result.vanilla import EmptyResult, Result
