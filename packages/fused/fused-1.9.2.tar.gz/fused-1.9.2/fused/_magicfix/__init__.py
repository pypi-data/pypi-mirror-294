"""isort:skip_file"""
# ruff: noqa: F401

from __future__ import annotations

import pandas

from .._udf.context import context

from fused._global_api import get_api
from fused.models.schema import Field, Schema

from fused.models.udf.output import Output as OutputModel

# We set pandas' 2.0 copy_on_write to ON by default to avoid pesky
# SettingWithCopyWarningErrors
pandas.options.mode.copy_on_write = True
