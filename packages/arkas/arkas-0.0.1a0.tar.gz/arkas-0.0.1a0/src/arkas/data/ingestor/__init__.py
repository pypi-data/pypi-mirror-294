r"""Contain the data ingestor."""

from __future__ import annotations

__all__ = ["BaseIngestor", "DataFrameIngestor", "Ingestor", "is_ingestor_config", "setup_ingestor"]

from arkas.data.ingestor.base import BaseIngestor, is_ingestor_config, setup_ingestor
from arkas.data.ingestor.dataframe import DataFrameIngestor
from arkas.data.ingestor.vanilla import Ingestor
