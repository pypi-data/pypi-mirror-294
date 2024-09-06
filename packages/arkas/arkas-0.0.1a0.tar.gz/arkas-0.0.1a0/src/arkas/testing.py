r"""Define some utility functions for testing."""

from __future__ import annotations

__all__ = ["colorlog_available", "markdown_available"]

import pytest

from arkas.utils.imports import is_colorlog_available, is_markdown_available

colorlog_available = pytest.mark.skipif(not is_colorlog_available(), reason="requires colorlog")
markdown_available = pytest.mark.skipif(not is_markdown_available(), reason="requires markdown")
