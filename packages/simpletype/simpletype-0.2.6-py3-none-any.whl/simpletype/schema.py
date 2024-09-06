# -*- coding: utf-8 -*-

"""
A simple schema definition system.
"""

import typing as T
import dataclasses
from datetime import datetime
from base64 import b64decode, b64encode

try:
    import polars as pl

    has_polars = True
except ImportError as e:  # pragma: no cover
    has_polars = False

try:
    import pyspark.sql.types as pst

    has_pyspark = True
except ImportError as e:  # pragma: no cover
    has_pyspark = False

from .sentinel import NOTHING, resolve_kwargs
from .constants import (
    TypeNameEnum,
    AwsDynamoDBTypeEnum,
    AwsGlueTypeEnum,
    SparkTypeEnum,
)

if T.TYPE_CHECKING:  # pragma: no cover
    from .typehint import T_SIMPLE_SCHEMA
    from .typehint import T_POLARS_SCHEMA
    from .typehint import T_SPARK_SCHEMA


def bin_to_b64str(b: bytes) -> str:
    return b64encode(b).decode("utf-8")


def b64str_to_bin(s: str) -> bytes:
    return b64decode(s.encode("utf-8"))


@dataclasses.dataclass
class BaseType:
    """
    Base class for all data types in simple schema system.
    """

    def to_dict(self) -> dict:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, dct: dict) -> "BaseType":
        return json_type_to_simple_type(json_type=dct)

    def to_polars(self) -> T.Union[pl.DataType]:
        """
        Generate the corresponding polars type for the value.

        For example, a string value "hello" should be ``pl.Utf8()``,
        """
        raise NotImplementedError

    def to_dynamodb_json_polars(self) -> pl.Struct:
        """
        Generate the corresponding polars type for the value in DynamoDB JSON format.

        For example, a string value "hello" should be ``{"S": "hello"}``,
        then the polars type should be ``pl.Struct({"S": pl.Utf8()})``.
        """
        raise NotImplementedError

    def to_glue(self) -> str:
        """
        Generate the corresponding "type" syntax for AWS Glue ``create_table``
        API call.

        Note that this is only the "type" part, not the full schema.

        For example, a Python ``name:str`` string type should be
        ``{"Name": "name", "Type": "string", "Comment": "..."}`` in create_table
        API call. This method only returns the ``"string"`` part.

        Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_table.html
        """
        raise NotImplementedError

    def to_pyspark(self) -> str:
        """
        Generate the corresponding pyspark type for the value.
        """
        raise NotImplementedError

    def to_spark_string(self) -> str:
        """
        Generate the corresponding "type" syntax for
        "spark.sql.sources.schema.part.0" parameter in Glue table schema.

        Note that this is only the "type" part, not the full schema.

        For example, a Python ``name:str`` string type should be
        ``{"name": "name", "type": "string", "nullable": true, "metadata": {}``
        in spark. This method only returns the ``"string"`` part.
        """
        raise NotImplementedError

    @property
    def classname(self) -> str:  # pragma: no cover
        return self.__class__.__name__


DATA_TYPE = T.TypeVar("DATA_TYPE", bound=BaseType)


@dataclasses.dataclass
class Integer(BaseType):
    """
    :param default_for_null: The default value for null for serialization.
    """

    default_for_null: T.Any = dataclasses.field(default=NOTHING)
    required: bool = dataclasses.field(default=False)

    def to_dict(self) -> dict:
        return resolve_kwargs(
            type=TypeNameEnum.int,
            default_for_null=self.default_for_null,
            required=self.required,
        )

    def to_polars(self) -> pl.Int32:
        return pl.Int32()

    def to_dynamodb_json_polars(self) -> pl.Struct:
        return pl.Struct({AwsDynamoDBTypeEnum.number: pl.Utf8()})

    def to_glue(self) -> str:
        return AwsGlueTypeEnum.bigint

    def to_spark_string(self) -> str:
        return SparkTypeEnum.bigint


@dataclasses.dataclass
class TinyInteger(BaseType):
    """
    :param default_for_null: The default value for null for serialization.
    """

    default_for_null: T.Any = dataclasses.field(default=NOTHING)
    required: bool = dataclasses.field(default=False)

    def to_dict(self) -> dict:
        return resolve_kwargs(
            type=TypeNameEnum.tinyint,
            default_for_null=self.default_for_null,
            required=self.required,
        )

    def to_polars(self) -> pl.Int8:
        return pl.Int8()

    def to_dynamodb_json_polars(self) -> pl.Struct:
        return pl.Struct({AwsDynamoDBTypeEnum.number: pl.Utf8()})

    def to_glue(self) -> str:
        return AwsGlueTypeEnum.tinyint

    def to_spark_string(self) -> str:
        return SparkTypeEnum.tinyint


@dataclasses.dataclass
class SmallInteger(BaseType):
    """
    :param default_for_null: The default value for null for serialization.
    """

    default_for_null: T.Any = dataclasses.field(default=NOTHING)
    required: bool = dataclasses.field(default=False)

    def to_dict(self) -> dict:
        return resolve_kwargs(
            type=TypeNameEnum.smallint,
            default_for_null=self.default_for_null,
            required=self.required,
        )

    def to_polars(self) -> pl.Int16:
        return pl.Int16()

    def to_dynamodb_json_polars(self) -> pl.Struct:
        return pl.Struct({AwsDynamoDBTypeEnum.number: pl.Utf8()})

    def to_glue(self) -> str:
        return AwsGlueTypeEnum.smallint

    def to_spark_string(self) -> str:
        return SparkTypeEnum.smallint


@dataclasses.dataclass
class BigInteger(BaseType):
    """
    :param default_for_null: The default value for null for serialization.
    """

    default_for_null: T.Any = dataclasses.field(default=NOTHING)
    required: bool = dataclasses.field(default=False)

    def to_dict(self) -> dict:
        return resolve_kwargs(
            type=TypeNameEnum.bigint,
            default_for_null=self.default_for_null,
            required=self.required,
        )

    def to_polars(self) -> pl.Int64:
        return pl.Int64()

    def to_dynamodb_json_polars(self) -> pl.Struct:
        return pl.Struct({AwsDynamoDBTypeEnum.number: pl.Utf8()})

    def to_glue(self) -> str:
        return AwsGlueTypeEnum.bigint

    def to_spark_string(self) -> str:
        return SparkTypeEnum.bigint


@dataclasses.dataclass
class Float(BaseType):
    """
    :param default_for_null: The default value for null for serialization
    :param precision: The number of decimal places to round to. If not set, no rounding is done.
    """

    default_for_null: T.Any = dataclasses.field(default=NOTHING)
    precision: int = dataclasses.field(default=NOTHING)
    required: bool = dataclasses.field(default=False)

    def to_dict(self) -> dict:
        return resolve_kwargs(
            type=TypeNameEnum.float,
            default_for_null=self.default_for_null,
            precision=self.precision,
            required=self.required,
        )

    def to_polars(self) -> pl.Float32:
        return pl.Float32()

    def to_dynamodb_json_polars(self) -> pl.Struct:
        return pl.Struct({AwsDynamoDBTypeEnum.number: pl.Utf8()})

    def to_glue(self) -> str:
        return AwsGlueTypeEnum.float

    def to_spark_string(self) -> str:
        return SparkTypeEnum.float


@dataclasses.dataclass
class Double(BaseType):
    """
    :param default_for_null: The default value for null for serialization
    :param precision: The number of decimal places to round to. If not set, no rounding is done.
    """

    default_for_null: T.Any = dataclasses.field(default=NOTHING)
    precision: int = dataclasses.field(default=NOTHING)
    required: bool = dataclasses.field(default=False)

    def to_dict(self) -> dict:
        return resolve_kwargs(
            type=TypeNameEnum.double,
            default_for_null=self.default_for_null,
            precision=self.precision,
            required=self.required,
        )

    def to_polars(self) -> pl.Float64:
        return pl.Float64()

    def to_dynamodb_json_polars(self) -> pl.Struct:
        return pl.Struct({AwsDynamoDBTypeEnum.number: pl.Utf8()})

    def to_glue(self) -> str:
        return AwsGlueTypeEnum.double

    def to_spark_string(self) -> str:
        return SparkTypeEnum.double


@dataclasses.dataclass
class Decimal(BaseType):
    """
    :param default_for_null: The default value for null for serialization
    """

    default_for_null: T.Any = dataclasses.field(default=NOTHING)
    required: bool = dataclasses.field(default=False)

    def to_dict(self) -> dict:
        return resolve_kwargs(
            type=TypeNameEnum.decimal,
            default_for_null=self.default_for_null,
            required=self.required,
        )

    def to_polars(self) -> pl.Decimal:
        return pl.Decimal()

    def to_dynamodb_json_polars(self) -> pl.Struct:
        return pl.Struct({AwsDynamoDBTypeEnum.number: pl.Utf8()})

    def to_glue(self) -> str:
        return AwsGlueTypeEnum.decimal

    def to_spark_string(self) -> str:
        return SparkTypeEnum.decimal


DEFAULT_NULL_STRING = ""
DEFAULT_NULL_BINARY = b""


@dataclasses.dataclass
class String(BaseType):
    """
    :param default_for_null: The default value for null for serialization.
    """

    default_for_null: T.Any = dataclasses.field(default=DEFAULT_NULL_STRING)
    required: bool = dataclasses.field(default=False)

    def to_dict(self) -> dict:
        return resolve_kwargs(
            type=TypeNameEnum.str,
            default_for_null=self.default_for_null,
            required=self.required,
        )

    def to_polars(self) -> pl.Utf8:
        return pl.Utf8()

    def to_dynamodb_json_polars(self) -> pl.Struct:
        return pl.Struct({AwsDynamoDBTypeEnum.string: pl.Utf8()})

    def to_glue(self) -> str:
        return AwsGlueTypeEnum.string

    def to_spark_string(self) -> str:
        return SparkTypeEnum.string


@dataclasses.dataclass
class Binary(BaseType):
    """
    :param default_for_null: The default value for null for serialization.
    """

    default_for_null: T.Any = dataclasses.field(default=DEFAULT_NULL_BINARY)
    required: bool = dataclasses.field(default=False)

    def to_dict(self) -> dict:
        if isinstance(self.default_for_null, bytes):
            default_for_null = bin_to_b64str(self.default_for_null)
        else:  # pragma: no cover
            default_for_null = self.default_for_null
        return resolve_kwargs(
            type=TypeNameEnum.bin,
            default_for_null=default_for_null,
            required=self.required,
        )

    def to_polars(self) -> pl.Binary:
        return pl.Binary()

    def to_dynamodb_json_polars(self) -> pl.Struct:
        return pl.Struct({AwsDynamoDBTypeEnum.binary: pl.Utf8()})

    def to_glue(self) -> str:
        return AwsGlueTypeEnum.binary

    def to_spark_string(self) -> str:
        return SparkTypeEnum.binary


@dataclasses.dataclass
class Bool(BaseType):
    """
    :param default_for_null: The default value for null for serialization
    """

    default_for_null: T.Any = dataclasses.field(default=NOTHING)
    required: bool = dataclasses.field(default=False)

    def to_dict(self) -> dict:
        return resolve_kwargs(
            type=TypeNameEnum.bool,
            default_for_null=self.default_for_null,
            required=self.required,
        )

    def to_polars(self) -> pl.Boolean:
        return pl.Boolean()

    def to_dynamodb_json_polars(self) -> pl.Struct:
        return pl.Struct({AwsDynamoDBTypeEnum.boolean: pl.Boolean()})

    def to_glue(self) -> str:
        return AwsGlueTypeEnum.boolean

    def to_spark_string(self) -> str:
        return SparkTypeEnum.boolean


@dataclasses.dataclass
class Null(BaseType):
    """
    :param default_for_null: The default value for null for serialization
    """

    default_for_null: T.Any = dataclasses.field(default=None)
    required: bool = dataclasses.field(default=False)

    def to_dict(self) -> dict:
        return resolve_kwargs(
            type=TypeNameEnum.null,
            default_for_null=self.default_for_null,
            required=self.required,
        )

    def to_polars(self) -> pl.Null:
        return pl.Null()

    def to_dynamodb_json_polars(self) -> pl.Struct:
        return pl.Struct({AwsDynamoDBTypeEnum.null: pl.Boolean()})

    def to_glue(self) -> str:
        return AwsGlueTypeEnum.string

    def to_spark_string(self) -> str:
        return SparkTypeEnum.null


@dataclasses.dataclass
class Datetime(BaseType):
    """
    :param default_for_null: The default value for null for serialization

    .. note::

        DynamoDB doesn't have a native datetime type. Don't use this type
        to describe DynamoDB schema. You can use it in anywhere else.

    """

    default_for_null: T.Any = dataclasses.field(default=NOTHING)
    required: bool = dataclasses.field(default=False)

    def to_dict(self) -> dict:
        if isinstance(self.default_for_null, datetime):
            default_for_null = self.default_for_null.isoformat()
        else:  # pragma: no cover
            default_for_null = self.default_for_null
        return resolve_kwargs(
            type=TypeNameEnum.datetime,
            default_for_null=default_for_null,
            required=self.required,
        )

    def to_polars(self) -> pl.Datetime:
        return pl.Datetime()

    def to_dynamodb_json_polars(self) -> pl.Struct:
        return pl.Struct({AwsDynamoDBTypeEnum.string: pl.Utf8()})

    def to_glue(self) -> str:
        return AwsGlueTypeEnum.timestamp

    def to_spark_string(self) -> str:
        return SparkTypeEnum.timestamp


@dataclasses.dataclass
class Set(BaseType):
    """
    Example::

        record = {"tags": ["a", "b", "c"]}

        schema = Struct({
            "tags": Set(String())
        })

    :param itype: The type of the elements in the set.
    """

    itype: BaseType = dataclasses.field(default=NOTHING)
    default_for_null: T.Any = dataclasses.field(default_factory=list)
    required: bool = dataclasses.field(default=False)

    def __post_init__(self):
        if self.itype is NOTHING:  # pragma: no cover
            raise ValueError("itype is required for Set")

    def to_dict(self) -> dict:
        return resolve_kwargs(
            type=TypeNameEnum.set,
            itype=self.itype.to_dict(),
            default_for_null=self.default_for_null,
            required=self.required,
        )

    def to_polars(self) -> pl.List:
        return pl.List(self.itype.to_polars())

    def to_dynamodb_json_polars(self) -> pl.Struct:
        if isinstance(self.itype, String):
            field = AwsDynamoDBTypeEnum.string_set
        elif isinstance(
            self.itype,
            (Integer, TinyInteger, SmallInteger, BigInteger, Float, Double, Decimal),
        ):
            field = AwsDynamoDBTypeEnum.number_set
        elif isinstance(self.itype, Binary):
            field = AwsDynamoDBTypeEnum.binary_set
        else:
            raise NotImplementedError
        return pl.Struct({field: pl.List(pl.Utf8())})

    def to_glue(self) -> str:
        return f"{AwsGlueTypeEnum.array}<{self.itype.to_glue()}>"

    def to_spark_string(self) -> dict:
        return {
            "type": SparkTypeEnum.array,
            "elementType": self.itype.to_spark_string(),
        }


@dataclasses.dataclass
class List(BaseType):
    """
    Example::

        record = {"tags": ["a", "b", "c"]}

        schema = Struct({
            "tags": List(String())
        })

    :param itype: The type of the elements in the list.
    """

    itype: BaseType = dataclasses.field(default=NOTHING)
    default_for_null: T.Any = dataclasses.field(default_factory=list)
    required: bool = dataclasses.field(default=False)

    def __post_init__(self):
        if self.itype is NOTHING:  # pragma: no cover
            raise ValueError("itype is required for List")

    def to_dict(self) -> dict:
        return resolve_kwargs(
            type=TypeNameEnum.list,
            itype=self.itype.to_dict(),
            default_for_null=self.default_for_null,
            required=self.required,
        )

    def to_polars(self) -> pl.List:
        return pl.List(self.itype.to_polars())

    def to_dynamodb_json_polars(self) -> pl.Struct:
        return pl.Struct(
            {AwsDynamoDBTypeEnum.list: pl.List(self.itype.to_dynamodb_json_polars())}
        )

    def to_glue(self) -> str:
        return f"{AwsGlueTypeEnum.array}<{self.itype.to_glue()}>"

    def to_spark_string(self) -> dict:
        return {
            "type": SparkTypeEnum.array,
            "elementType": self.itype.to_spark_string(),
            "containsNull": True,
        }


@dataclasses.dataclass
class Struct(BaseType):
    """
    Example:

        record = {
            "details": {
                "name": "Alice",
                "age": 30,
            }
        }

        schema = Struct({
            "details": Struct({
                "name": String(),
                "age": Integer(),
            })
        }),

    :param types: The types of the fields in the struct.
    """

    fields: T.Dict[str, BaseType] = dataclasses.field(default=NOTHING)
    required: bool = dataclasses.field(default=False)

    def __post_init__(self):
        if self.fields is NOTHING:  # pragma: no cover
            raise ValueError("types is required for Struct")

    def to_dict(self) -> dict:
        return resolve_kwargs(
            type=TypeNameEnum.struct,
            fields={k: v.to_dict() for k, v in self.fields.items()},
            required=self.required,
        )

    def to_polars(self) -> pl.Struct:
        return pl.Struct({k: v.to_polars() for k, v in self.fields.items()})

    def to_dynamodb_json_polars(self) -> pl.Struct:
        return pl.Struct(
            {
                AwsDynamoDBTypeEnum.map: pl.Struct(
                    {k: v.to_dynamodb_json_polars() for k, v in self.fields.items()}
                )
            }
        )

    def to_glue(self) -> str:
        """
        Ref: https://stackoverflow.com/questions/75763367/how-to-define-aws-glue-table-structure-with-embedded-structs
        """
        parts = [f"{k}:{v.to_glue()}" for k, v in self.fields.items()]
        struct_schema = ",".join(parts)
        return f"{AwsGlueTypeEnum.struct}<{struct_schema}>"

    def to_spark_string(self) -> dict:
        return {
            "type": SparkTypeEnum.struct,
            "fields": [
                {
                    "name": k,
                    "type": v.to_spark_string(),
                    "nullable": True,
                    "metadata": {},
                }
                for k, v in self.fields.items()
            ],
        }


def json_type_to_simple_type(
    json_type: T.Dict[str, T.Any],
) -> "DATA_TYPE":
    """
    Convert a JSON type definition to a simple type.

    >>> json_type_to_simple_type({"type": "int"})
    Integer()
    >>> json_type_to_simple_type({"type": "float"})
    Float()
    >>> json_type_to_simple_type({"type": "str"})
    String()
    >>> json_type_to_simple_type({"type": "bin"})
    Binary()
    >>> json_type_to_simple_type({"type": "bool"})
    Bool()
    >>> json_type_to_simple_type({"type": "null"})
    Null()

    >>> json_type_to_simple_type({"type": "set", "item": {"type": "int"}})
    Set(Integer())
    >>> json_type_to_simple_type({"type": "set", "item": {"type": "float"}})
    Set(Float())
    >>> json_type_to_simple_type({"type": "set", "item": {"type": "str"}})
    Set(String())
    >>> json_type_to_simple_type({"type": "set", "item": {"type": "bin"}})
    Set(Binary())

    >>> json_type_to_simple_type({"type": "list", "item": {"type": "int"}})
    List(Integer())
    >>> json_type_to_simple_type({"type": "list", "item": {"type": "float"}})
    List(Float())
    >>> json_type_to_simple_type({"type": "list", "item": {"type": "str"}})
    List(String())
    >>> json_type_to_simple_type({"type": "list", "item": {"type": "bin"}})
    List(Binary())

    >>> json_type_to_simple_type({
    ...     "type": "list",
    ...     "item": {"type": "map", "values": {"a_int": {"type": "int"}}}
    ... })
    List(Struct({"a_int": Integer()}))

    >>> json_type_to_simple_type({
    ...     "type": "map",
    ...     "values": {
    ...         "a_int": {"type": "int"},
    ...         "a_str": {"type": "str"},
    ...         "a_list_of_int": {"type": "list", "item": {"type": "int"}},
    ...         "a_set_of_str": {"type": "set", "item": {"type": "str"}},
    ...     },
    ... })
    Struct({
        "a_int": Integer(),
        "a_str": String(),
        "a_list_of_int": List(Integer()),
        "a_set_of_str": Set(String()),
    })
    """
    kwargs = dict()
    if "default_for_null" in json_type:  # pragma: no cover
        kwargs["default_for_null"] = json_type["default_for_null"]

    if json_type["type"] == TypeNameEnum.int:
        return Integer(**kwargs)
    elif json_type["type"] == TypeNameEnum.tinyint:
        return TinyInteger(**kwargs)
    elif json_type["type"] == TypeNameEnum.smallint:
        return SmallInteger(**kwargs)
    elif json_type["type"] == TypeNameEnum.bigint:
        return BigInteger(**kwargs)
    elif json_type["type"] == TypeNameEnum.float:
        return Float(**kwargs)
    elif json_type["type"] == TypeNameEnum.double:
        return Double(**kwargs)
    elif json_type["type"] == TypeNameEnum.decimal:
        return Decimal(**kwargs)
    elif json_type["type"] == TypeNameEnum.str:
        return String(**kwargs)
    elif json_type["type"] == TypeNameEnum.bin:
        if "default_for_null" in kwargs:
            if isinstance(kwargs["default_for_null"], str):
                kwargs["default_for_null"] = b64str_to_bin(kwargs["default_for_null"])
        return Binary(**kwargs)
    elif json_type["type"] == TypeNameEnum.bool:
        return Bool(**kwargs)
    elif json_type["type"] == TypeNameEnum.null:
        return Null(**kwargs)
    elif json_type["type"] == TypeNameEnum.datetime:
        if "default_for_null" in kwargs:
            if isinstance(kwargs["default_for_null"], str):
                kwargs["default_for_null"] = datetime.fromisoformat(
                    kwargs["default_for_null"]
                )
        return Datetime(**kwargs)
    elif json_type["type"] == TypeNameEnum.set:
        return Set(itype=json_type_to_simple_type(json_type["itype"]), **kwargs)
    elif json_type["type"] == TypeNameEnum.list:
        return List(itype=json_type_to_simple_type(json_type["itype"]), **kwargs)
    elif json_type["type"] == TypeNameEnum.struct:
        schema = dict()
        for k, v in json_type["fields"].items():
            schema[k] = json_type_to_simple_type(v)
        return Struct(fields=schema, **kwargs)
    else:  # pragma: no cover
        raise NotImplementedError


def polars_type_to_simple_type(
    p_type: "pl.DataType",
) -> DATA_TYPE:  # pragma: no cover
    if isinstance(p_type, pl.Int32):
        return Integer()
    elif isinstance(p_type, pl.Int8):
        return TinyInteger()
    elif isinstance(p_type, pl.Int16):
        return SmallInteger()
    elif isinstance(p_type, pl.Int64):
        return BigInteger()
    elif isinstance(p_type, pl.Float32):
        return Float()
    elif isinstance(p_type, pl.Float64):
        return Double()
    elif isinstance(p_type, pl.Decimal):
        return Decimal()
    elif isinstance(p_type, pl.String):
        return String()
    elif isinstance(p_type, pl.Binary):
        return Binary()
    elif isinstance(p_type, pl.Boolean):
        return Bool()
    elif isinstance(p_type, pl.Null):
        return Null()
    elif isinstance(p_type, pl.Datetime):
        return Datetime()
    elif isinstance(p_type, pl.List):
        return List(itype=polars_type_to_simple_type(p_type.inner))
    elif isinstance(p_type, pl.Struct):
        fields = {
            field.name: polars_type_to_simple_type(field.dtype)
            for field in p_type.fields
        }
        return Struct(fields=fields)
    else:
        raise NotImplementedError
