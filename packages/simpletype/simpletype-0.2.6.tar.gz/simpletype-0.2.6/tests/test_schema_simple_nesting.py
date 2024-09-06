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
    Datetime,
    Set,
    List,
    Struct,
    json_type_to_simple_type,
)


def test_list_of_integer():
    list_int_type = json_type_to_simple_type(
        {"type": TypeNameEnum.list, "itype": {"type": TypeNameEnum.int}}
    )
    assert isinstance(list_int_type, List)
    assert isinstance(list_int_type.itype, Integer)
    assert list_int_type.to_polars() == pl.List(pl.Int32())
    assert list_int_type.to_dynamodb_json_polars() == pl.Struct(
        {"L": pl.List(pl.Struct({"N": pl.Utf8()}))}
    )
    assert (
        list_int_type.to_glue() == f"{AwsGlueTypeEnum.array}<{AwsGlueTypeEnum.bigint}>"
    )
    assert list_int_type.to_spark_string() == {
        "type": SparkTypeEnum.array,
        "elementType": SparkTypeEnum.bigint,
        "containsNull": True,
    }


def test_list_of_float():
    list_float_type = json_type_to_simple_type(
        {"type": TypeNameEnum.list, "itype": {"type": TypeNameEnum.float}}
    )
    assert isinstance(list_float_type, List)
    assert isinstance(list_float_type.itype, Float)
    assert list_float_type.to_polars() == pl.List(pl.Float32())
    assert list_float_type.to_dynamodb_json_polars() == pl.Struct(
        {"L": pl.List(pl.Struct({"N": pl.Utf8()}))}
    )
    assert (
        list_float_type.to_glue() == f"{AwsGlueTypeEnum.array}<{AwsGlueTypeEnum.float}>"
    )
    assert list_float_type.to_spark_string() == {
        "type": SparkTypeEnum.array,
        "elementType": SparkTypeEnum.float,
        "containsNull": True,
    }


def test_list_of_datetime():
    list_datetime_type = json_type_to_simple_type(
        {"type": TypeNameEnum.list, "itype": {"type": TypeNameEnum.datetime}}
    )
    assert isinstance(list_datetime_type, List)
    assert isinstance(list_datetime_type.itype, Datetime)
    assert list_datetime_type.to_polars() == pl.List(pl.Datetime())
    assert list_datetime_type.to_dynamodb_json_polars() == pl.Struct(
        {"L": pl.List(pl.Struct({"S": pl.Utf8()}))}
    )
    assert (
        list_datetime_type.to_glue()
        == f"{AwsGlueTypeEnum.array}<{AwsGlueTypeEnum.timestamp}>"
    )
    assert list_datetime_type.to_spark_string() == {
        "type": SparkTypeEnum.array,
        "elementType": SparkTypeEnum.timestamp,
        "containsNull": True,
    }


def test_set_of_integer():
    set_int_type = json_type_to_simple_type(
        {"type": TypeNameEnum.set, "itype": {"type": TypeNameEnum.int}}
    )
    assert isinstance(set_int_type, Set)
    assert isinstance(set_int_type.itype, Integer)
    assert set_int_type.to_polars() == pl.List(pl.Int32())
    assert set_int_type.to_dynamodb_json_polars() == pl.Struct(
        {"NS": pl.List(pl.Utf8())}
    )
    assert (
        set_int_type.to_glue() == f"{AwsGlueTypeEnum.array}<{AwsGlueTypeEnum.bigint}>"
    )
    assert set_int_type.to_spark_string() == {
        "type": SparkTypeEnum.array,
        "elementType": SparkTypeEnum.bigint,
    }


def test_set_of_float():
    set_float_type = json_type_to_simple_type(
        {"type": TypeNameEnum.set, "itype": {"type": TypeNameEnum.float}}
    )
    assert isinstance(set_float_type, Set)
    assert isinstance(set_float_type.itype, Float)
    assert set_float_type.to_polars() == pl.List(pl.Float32())
    assert set_float_type.to_dynamodb_json_polars() == pl.Struct(
        {"NS": pl.List(pl.Utf8())}
    )
    assert (
        set_float_type.to_glue() == f"{AwsGlueTypeEnum.array}<{AwsGlueTypeEnum.float}>"
    )
    assert set_float_type.to_spark_string() == {
        "type": SparkTypeEnum.array,
        "elementType": SparkTypeEnum.float,
    }


def test_set_of_string():
    set_string_type = json_type_to_simple_type(
        {"type": TypeNameEnum.set, "itype": {"type": TypeNameEnum.str}}
    )
    assert isinstance(set_string_type, Set)
    assert isinstance(set_string_type.itype, String)
    assert set_string_type.to_polars() == pl.List(pl.Utf8())
    assert set_string_type.to_dynamodb_json_polars() == pl.Struct(
        {"SS": pl.List(pl.Utf8())}
    )
    assert (
        set_string_type.to_glue()
        == f"{AwsGlueTypeEnum.array}<{AwsGlueTypeEnum.string}>"
    )
    assert set_string_type.to_spark_string() == {
        "type": SparkTypeEnum.array,
        "elementType": SparkTypeEnum.string,
    }


def test_set_of_binary():
    set_binary_type = json_type_to_simple_type(
        {"type": TypeNameEnum.set, "itype": {"type": TypeNameEnum.bin}}
    )
    assert isinstance(set_binary_type, Set)
    assert isinstance(set_binary_type.itype, Binary)
    assert set_binary_type.to_polars() == pl.List(pl.Binary())
    assert set_binary_type.to_dynamodb_json_polars() == pl.Struct(
        {"BS": pl.List(pl.Utf8())}
    )
    assert (
        set_binary_type.to_glue()
        == f"{AwsGlueTypeEnum.array}<{AwsGlueTypeEnum.binary}>"
    )
    assert set_binary_type.to_spark_string() == {
        "type": SparkTypeEnum.array,
        "elementType": SparkTypeEnum.binary,
    }


def test_struct_of_simple_types():
    struct_type = json_type_to_simple_type(
        {
            "type": TypeNameEnum.struct,
            "fields": {
                "int_field": {"type": TypeNameEnum.int},
                "float_field": {"type": TypeNameEnum.float},
                "string_field": {"type": TypeNameEnum.str},
            },
        }
    )
    assert isinstance(struct_type, Struct)
    assert isinstance(struct_type.fields["int_field"], Integer)
    assert isinstance(struct_type.fields["float_field"], Float)
    assert isinstance(struct_type.fields["string_field"], String)
    assert struct_type.to_polars() == pl.Struct(
        {
            "int_field": pl.Int32(),
            "float_field": pl.Float32(),
            "string_field": pl.Utf8(),
        }
    )
    assert struct_type.to_dynamodb_json_polars() == pl.Struct(
        {
            "M": pl.Struct(
                {
                    "int_field": pl.Struct({"N": pl.Utf8()}),
                    "float_field": pl.Struct({"N": pl.Utf8()}),
                    "string_field": pl.Struct({"S": pl.Utf8()}),
                }
            )
        }
    )
    assert (
        struct_type.to_glue()
        == f"{AwsGlueTypeEnum.struct}<int_field:{AwsGlueTypeEnum.bigint},float_field:{AwsGlueTypeEnum.float},string_field:{AwsGlueTypeEnum.string}>"
    )
    assert struct_type.to_spark_string() == {
        "type": SparkTypeEnum.struct,
        "fields": [
            {
                "name": "int_field",
                "type": SparkTypeEnum.bigint,
                "nullable": True,
                "metadata": {},
            },
            {
                "name": "float_field",
                "type": SparkTypeEnum.float,
                "nullable": True,
                "metadata": {},
            },
            {
                "name": "string_field",
                "type": SparkTypeEnum.string,
                "nullable": True,
                "metadata": {},
            },
        ],
    }


def test_struct_with_nested_list():
    struct_with_list_type = json_type_to_simple_type(
        {
            "type": TypeNameEnum.struct,
            "fields": {
                "int_field": {"type": TypeNameEnum.int},
                "list_field": {
                    "type": TypeNameEnum.list,
                    "itype": {"type": TypeNameEnum.float},
                },
            },
        }
    )
    assert isinstance(struct_with_list_type, Struct)
    assert isinstance(struct_with_list_type.fields["int_field"], Integer)
    assert isinstance(struct_with_list_type.fields["list_field"], List)
    assert isinstance(struct_with_list_type.fields["list_field"].itype, Float)
    assert struct_with_list_type.to_polars() == pl.Struct(
        {
            "int_field": pl.Int32(),
            "list_field": pl.List(pl.Float32()),
        }
    )
    assert struct_with_list_type.to_dynamodb_json_polars() == pl.Struct(
        {
            "M": pl.Struct(
                {
                    "int_field": pl.Struct({"N": pl.Utf8()}),
                    "list_field": pl.Struct(
                        {"L": pl.List(pl.Struct({"N": pl.Utf8()}))}
                    ),
                }
            )
        }
    )
    assert (
        struct_with_list_type.to_glue()
        == f"{AwsGlueTypeEnum.struct}<int_field:{AwsGlueTypeEnum.bigint},list_field:{AwsGlueTypeEnum.array}<{AwsGlueTypeEnum.float}>>"
    )
    assert struct_with_list_type.to_spark_string() == {
        "type": SparkTypeEnum.struct,
        "fields": [
            {
                "name": "int_field",
                "type": SparkTypeEnum.bigint,
                "nullable": True,
                "metadata": {},
            },
            {
                "name": "list_field",
                "type": {
                    "type": SparkTypeEnum.array,
                    "elementType": SparkTypeEnum.float,
                    "containsNull": True,
                },
                "nullable": True,
                "metadata": {},
            },
        ],
    }


if __name__ == "__main__":
    from simpletype.tests import run_cov_test

    run_cov_test(__file__, "simpletype.schema", preview=False)
