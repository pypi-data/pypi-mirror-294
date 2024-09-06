# -*- coding: utf-8 -*-

import typing as T

if T.TYPE_CHECKING:  # pragma: no cover
    from .schema import DATA_TYPE
    import polars as pl
    import pyspark.sql.types as pst

T_SIMPLE_SCHEMA = T.Dict[str, "DATA_TYPE"]
T_POLARS_SCHEMA = T.Dict[str, "pl.DataType"]
T_SPARK_SCHEMA = T.Dict[str, "pst.DataType"]
