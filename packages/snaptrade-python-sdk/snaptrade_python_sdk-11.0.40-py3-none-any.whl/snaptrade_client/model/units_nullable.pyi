# coding: utf-8

"""
    SnapTrade

    Connect brokerage accounts to your app for live positions and trading

    The version of the OpenAPI document: 1.0.0
    Contact: api@snaptrade.com
    Created by: https://snaptrade.com/
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from snaptrade_client import schemas  # noqa: F401


class UnitsNullable(
    schemas.NumberBase,
    schemas.NoneBase,
    schemas.Schema,
    schemas.NoneDecimalMixin
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)

    Number of shares for the order. This can be a decimal for fractional orders. Must be `null` if `notional_value` is provided.
    """


    def __new__(
        cls,
        *args: typing.Union[None, decimal.Decimal, int, float, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
    ) -> 'UnitsNullable':
        return super().__new__(
            cls,
            *args,
            _configuration=_configuration,
        )
