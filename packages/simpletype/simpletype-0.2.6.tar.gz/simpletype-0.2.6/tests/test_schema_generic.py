# -*- coding: utf-8 -*-

import polars as pl
from simpletype.schema import (
    TypeNameEnum,
    AwsGlueTypeEnum,
    SparkTypeEnum,
    Integer,
    TinyInteger,
    SmallInteger,
    BigInteger,
    Float,
    Double,
    Decimal,
    String,
    Binary,
    Bool,
    Null,
    Set,
    List,
    Struct,
    json_type_to_simple_type,
)


def test_integer():
    integer_type = json_type_to_simple_type({"type": TypeNameEnum.int})
    assert integer_type.to_polars() == pl.Int32()
    assert integer_type.to_dynamodb_json_polars() == pl.Struct({"N": pl.Utf8()})
    assert integer_type.to_glue() == AwsGlueTypeEnum.bigint
    assert integer_type.to_spark_string() == AwsGlueTypeEnum.bigint


def test_tiny_integer():
    tiny_integer_type = json_type_to_simple_type({"type": TypeNameEnum.tinyint})
    assert tiny_integer_type.to_polars() == pl.Int8()
    assert tiny_integer_type.to_dynamodb_json_polars() == pl.Struct({"N": pl.Utf8()})
    assert tiny_integer_type.to_glue() == AwsGlueTypeEnum.tinyint
    assert tiny_integer_type.to_spark_string() == SparkTypeEnum.tinyint


def test_small_integer():
    small_integer_type = json_type_to_simple_type({"type": TypeNameEnum.smallint})
    assert small_integer_type.to_polars() == pl.Int16()
    assert small_integer_type.to_dynamodb_json_polars() == pl.Struct({"N": pl.Utf8()})
    assert small_integer_type.to_glue() == AwsGlueTypeEnum.smallint
    assert small_integer_type.to_spark_string() == SparkTypeEnum.smallint


def test_big_integer():
    big_integer_type = json_type_to_simple_type({"type": TypeNameEnum.bigint})
    assert big_integer_type.to_polars() == pl.Int64()
    assert big_integer_type.to_dynamodb_json_polars() == pl.Struct({"N": pl.Utf8()})
    assert big_integer_type.to_glue() == AwsGlueTypeEnum.bigint
    assert big_integer_type.to_spark_string() == SparkTypeEnum.bigint


def test_float():
    float_type = json_type_to_simple_type({"type": TypeNameEnum.float})
    assert float_type.to_polars() == pl.Float32()
    assert float_type.to_dynamodb_json_polars() == pl.Struct({"N": pl.Utf8()})
    assert float_type.to_glue() == AwsGlueTypeEnum.float
    assert float_type.to_spark_string() == SparkTypeEnum.float


def test_double():
    double_type = json_type_to_simple_type({"type": TypeNameEnum.double})
    assert double_type.to_polars() == pl.Float64()
    assert double_type.to_dynamodb_json_polars() == pl.Struct({"N": pl.Utf8()})
    assert double_type.to_glue() == AwsGlueTypeEnum.double
    assert double_type.to_spark_string() == SparkTypeEnum.double


def test_decimal():
    decimal_type = json_type_to_simple_type({"type": TypeNameEnum.decimal})
    assert decimal_type.to_polars() == pl.Decimal()
    assert decimal_type.to_dynamodb_json_polars() == pl.Struct({"N": pl.Utf8()})
    assert decimal_type.to_glue() == AwsGlueTypeEnum.decimal
    assert decimal_type.to_spark_string() == SparkTypeEnum.decimal


def test_string():
    string_type = json_type_to_simple_type({"type": TypeNameEnum.str})
    assert string_type.to_polars() == pl.Utf8()
    assert string_type.to_dynamodb_json_polars() == pl.Struct({"S": pl.Utf8()})
    assert string_type.to_glue() == AwsGlueTypeEnum.string
    assert string_type.to_spark_string() == SparkTypeEnum.string
    assert string_type.default_for_null == ""


def test_binary():
    binary_type = json_type_to_simple_type({"type": TypeNameEnum.bin})
    assert binary_type.to_polars() == pl.Binary()
    assert binary_type.to_dynamodb_json_polars() == pl.Struct({"B": pl.Utf8()})
    assert binary_type.to_glue() == AwsGlueTypeEnum.binary
    assert binary_type.to_spark_string() == SparkTypeEnum.binary
    assert binary_type.default_for_null == b""


def test_bool():
    bool_type = json_type_to_simple_type({"type": TypeNameEnum.bool})
    assert bool_type.to_polars() == pl.Boolean()
    assert bool_type.to_dynamodb_json_polars() == pl.Struct({"BOOL": pl.Boolean()})
    assert bool_type.to_glue() == AwsGlueTypeEnum.boolean
    assert bool_type.to_spark_string() == SparkTypeEnum.boolean


def test_null():
    null_type = json_type_to_simple_type({"type": TypeNameEnum.null})
    assert null_type.to_polars() == pl.Null()
    assert null_type.to_dynamodb_json_polars() == pl.Struct({"NULL": pl.Boolean()})
    assert null_type.to_glue() == AwsGlueTypeEnum.string
    assert null_type.to_spark_string() == SparkTypeEnum.null
    assert null_type.default_for_null is None


def test_datetime():
    datetime_type = json_type_to_simple_type({"type": TypeNameEnum.datetime})
    assert datetime_type.to_polars() == pl.Datetime()
    assert datetime_type.to_dynamodb_json_polars() == pl.Struct({"S": pl.Utf8()})
    assert datetime_type.to_glue() == AwsGlueTypeEnum.timestamp
    assert datetime_type.to_spark_string() == SparkTypeEnum.timestamp


if __name__ == "__main__":
    from simpletype.tests import run_cov_test

    run_cov_test(__file__, "simpletype.schema", preview=False)
