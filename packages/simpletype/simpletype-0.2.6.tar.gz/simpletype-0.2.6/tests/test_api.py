# -*- coding: utf-8 -*-

from simpletype import api


def test():
    _ = api
    _ = api.T_SIMPLE_SCHEMA
    _ = api.T_POLARS_SCHEMA
    _ = api.T_SPARK_SCHEMA
    _ = api.TypeAttrEnum
    _ = api.TypeNameEnum
    _ = api.AwsDynamoDBTypeEnum
    _ = api.AwsGlueTypeEnum
    _ = api.SparkTypeEnum
    _ = api.BaseType
    _ = api.DATA_TYPE
    _ = api.Integer
    _ = api.TinyInteger
    _ = api.SmallInteger
    _ = api.BigInteger
    _ = api.Float
    _ = api.Double
    _ = api.Decimal
    _ = api.String
    _ = api.Binary
    _ = api.Bool
    _ = api.Null
    _ = api.Datetime
    _ = api.Set
    _ = api.List
    _ = api.Struct
    _ = api.json_type_to_simple_type
    _ = api.polars_type_to_simple_type

    _ = api.BaseType.from_dict
    _ = api.BaseType.to_dict
    _ = api.BaseType.to_polars
    _ = api.BaseType.to_dynamodb_json_polars
    _ = api.BaseType.to_glue
    _ = api.BaseType.to_spark_string


if __name__ == "__main__":
    from simpletype.tests import run_cov_test

    run_cov_test(__file__, "simpletype.api", preview=False)
