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


class AccountOrderRecord(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)

    Describes a single recent order in an account. Each record here represents a single order leg. For multi-leg orders, there will be multiple records.
    """


    class MetaOapg:
        
        class properties:
            brokerage_order_id = schemas.StrSchema
        
            @staticmethod
            def status() -> typing.Type['AccountOrderRecordStatus']:
                return AccountOrderRecordStatus
            symbol = schemas.UUIDSchema
            
            
            class universal_symbol(
                schemas.ComposedSchema,
            ):
            
            
                class MetaOapg:
                    
                    @classmethod
                    @functools.lru_cache()
                    def all_of(cls):
                        # we need this here to make our import statements work
                        # we must store _composed_schemas in here so the code is only run
                        # when we invoke this method. If we kept this at the class
                        # level we would get an error because the class level
                        # code would be run when this module is imported, and these composed
                        # classes don't exist yet because their module has not finished
                        # loading
                        return [
                            UniversalSymbol,
                        ]
            
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'universal_symbol':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            
            
            class option_symbol(
                schemas.ComposedSchema,
            ):
            
            
                class MetaOapg:
                    
                    @classmethod
                    @functools.lru_cache()
                    def all_of(cls):
                        # we need this here to make our import statements work
                        # we must store _composed_schemas in here so the code is only run
                        # when we invoke this method. If we kept this at the class
                        # level we would get an error because the class level
                        # code would be run when this module is imported, and these composed
                        # classes don't exist yet because their module has not finished
                        # loading
                        return [
                            OptionsSymbol,
                        ]
            
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'option_symbol':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            action = schemas.StrSchema
            
            
            class total_quantity(
                schemas.NumberBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, decimal.Decimal, int, float, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'total_quantity':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            
            
            class open_quantity(
                schemas.NumberBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, decimal.Decimal, int, float, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'open_quantity':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            
            
            class canceled_quantity(
                schemas.NumberBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, decimal.Decimal, int, float, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'canceled_quantity':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            
            
            class filled_quantity(
                schemas.NumberBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, decimal.Decimal, int, float, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'filled_quantity':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            
            
            class execution_price(
                schemas.NumberBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, decimal.Decimal, int, float, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'execution_price':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            
            
            class limit_price(
                schemas.NumberBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, decimal.Decimal, int, float, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'limit_price':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            
            
            class stop_price(
                schemas.NumberBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, decimal.Decimal, int, float, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'stop_price':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            
            
            class order_type(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'order_type':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            time_in_force = schemas.StrSchema
            time_placed = schemas.DateTimeSchema
            
            
            class time_updated(
                schemas.DateTimeBase,
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                class MetaOapg:
                    format = 'date-time'
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, str, datetime, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'time_updated':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            
            
            class time_executed(
                schemas.DateTimeBase,
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                class MetaOapg:
                    format = 'date-time'
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, str, datetime, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'time_executed':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            
            
            class expiry_date(
                schemas.DateTimeBase,
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                class MetaOapg:
                    format = 'date-time'
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, str, datetime, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'expiry_date':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            __annotations__ = {
                "brokerage_order_id": brokerage_order_id,
                "status": status,
                "symbol": symbol,
                "universal_symbol": universal_symbol,
                "option_symbol": option_symbol,
                "action": action,
                "total_quantity": total_quantity,
                "open_quantity": open_quantity,
                "canceled_quantity": canceled_quantity,
                "filled_quantity": filled_quantity,
                "execution_price": execution_price,
                "limit_price": limit_price,
                "stop_price": stop_price,
                "order_type": order_type,
                "time_in_force": time_in_force,
                "time_placed": time_placed,
                "time_updated": time_updated,
                "time_executed": time_executed,
                "expiry_date": expiry_date,
            }
        additional_properties = schemas.AnyTypeSchema
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["brokerage_order_id"]) -> MetaOapg.properties.brokerage_order_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> 'AccountOrderRecordStatus': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["symbol"]) -> MetaOapg.properties.symbol: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["universal_symbol"]) -> MetaOapg.properties.universal_symbol: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["option_symbol"]) -> MetaOapg.properties.option_symbol: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["action"]) -> MetaOapg.properties.action: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["total_quantity"]) -> MetaOapg.properties.total_quantity: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["open_quantity"]) -> MetaOapg.properties.open_quantity: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["canceled_quantity"]) -> MetaOapg.properties.canceled_quantity: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["filled_quantity"]) -> MetaOapg.properties.filled_quantity: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["execution_price"]) -> MetaOapg.properties.execution_price: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["limit_price"]) -> MetaOapg.properties.limit_price: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["stop_price"]) -> MetaOapg.properties.stop_price: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["order_type"]) -> MetaOapg.properties.order_type: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["time_in_force"]) -> MetaOapg.properties.time_in_force: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["time_placed"]) -> MetaOapg.properties.time_placed: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["time_updated"]) -> MetaOapg.properties.time_updated: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["time_executed"]) -> MetaOapg.properties.time_executed: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["expiry_date"]) -> MetaOapg.properties.expiry_date: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> MetaOapg.additional_properties: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["brokerage_order_id"], typing_extensions.Literal["status"], typing_extensions.Literal["symbol"], typing_extensions.Literal["universal_symbol"], typing_extensions.Literal["option_symbol"], typing_extensions.Literal["action"], typing_extensions.Literal["total_quantity"], typing_extensions.Literal["open_quantity"], typing_extensions.Literal["canceled_quantity"], typing_extensions.Literal["filled_quantity"], typing_extensions.Literal["execution_price"], typing_extensions.Literal["limit_price"], typing_extensions.Literal["stop_price"], typing_extensions.Literal["order_type"], typing_extensions.Literal["time_in_force"], typing_extensions.Literal["time_placed"], typing_extensions.Literal["time_updated"], typing_extensions.Literal["time_executed"], typing_extensions.Literal["expiry_date"], str, ]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["brokerage_order_id"]) -> typing.Union[MetaOapg.properties.brokerage_order_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> typing.Union['AccountOrderRecordStatus', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["symbol"]) -> typing.Union[MetaOapg.properties.symbol, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["universal_symbol"]) -> typing.Union[MetaOapg.properties.universal_symbol, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["option_symbol"]) -> typing.Union[MetaOapg.properties.option_symbol, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["action"]) -> typing.Union[MetaOapg.properties.action, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["total_quantity"]) -> typing.Union[MetaOapg.properties.total_quantity, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["open_quantity"]) -> typing.Union[MetaOapg.properties.open_quantity, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["canceled_quantity"]) -> typing.Union[MetaOapg.properties.canceled_quantity, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["filled_quantity"]) -> typing.Union[MetaOapg.properties.filled_quantity, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["execution_price"]) -> typing.Union[MetaOapg.properties.execution_price, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["limit_price"]) -> typing.Union[MetaOapg.properties.limit_price, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["stop_price"]) -> typing.Union[MetaOapg.properties.stop_price, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["order_type"]) -> typing.Union[MetaOapg.properties.order_type, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["time_in_force"]) -> typing.Union[MetaOapg.properties.time_in_force, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["time_placed"]) -> typing.Union[MetaOapg.properties.time_placed, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["time_updated"]) -> typing.Union[MetaOapg.properties.time_updated, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["time_executed"]) -> typing.Union[MetaOapg.properties.time_executed, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["expiry_date"]) -> typing.Union[MetaOapg.properties.expiry_date, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[MetaOapg.additional_properties, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["brokerage_order_id"], typing_extensions.Literal["status"], typing_extensions.Literal["symbol"], typing_extensions.Literal["universal_symbol"], typing_extensions.Literal["option_symbol"], typing_extensions.Literal["action"], typing_extensions.Literal["total_quantity"], typing_extensions.Literal["open_quantity"], typing_extensions.Literal["canceled_quantity"], typing_extensions.Literal["filled_quantity"], typing_extensions.Literal["execution_price"], typing_extensions.Literal["limit_price"], typing_extensions.Literal["stop_price"], typing_extensions.Literal["order_type"], typing_extensions.Literal["time_in_force"], typing_extensions.Literal["time_placed"], typing_extensions.Literal["time_updated"], typing_extensions.Literal["time_executed"], typing_extensions.Literal["expiry_date"], str, ]):
        return super().get_item_oapg(name)

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        brokerage_order_id: typing.Union[MetaOapg.properties.brokerage_order_id, str, schemas.Unset] = schemas.unset,
        status: typing.Union['AccountOrderRecordStatus', schemas.Unset] = schemas.unset,
        symbol: typing.Union[MetaOapg.properties.symbol, str, uuid.UUID, schemas.Unset] = schemas.unset,
        universal_symbol: typing.Union[MetaOapg.properties.universal_symbol, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        option_symbol: typing.Union[MetaOapg.properties.option_symbol, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        action: typing.Union[MetaOapg.properties.action, str, schemas.Unset] = schemas.unset,
        total_quantity: typing.Union[MetaOapg.properties.total_quantity, None, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        open_quantity: typing.Union[MetaOapg.properties.open_quantity, None, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        canceled_quantity: typing.Union[MetaOapg.properties.canceled_quantity, None, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        filled_quantity: typing.Union[MetaOapg.properties.filled_quantity, None, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        execution_price: typing.Union[MetaOapg.properties.execution_price, None, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        limit_price: typing.Union[MetaOapg.properties.limit_price, None, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        stop_price: typing.Union[MetaOapg.properties.stop_price, None, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        order_type: typing.Union[MetaOapg.properties.order_type, None, str, schemas.Unset] = schemas.unset,
        time_in_force: typing.Union[MetaOapg.properties.time_in_force, str, schemas.Unset] = schemas.unset,
        time_placed: typing.Union[MetaOapg.properties.time_placed, str, datetime, schemas.Unset] = schemas.unset,
        time_updated: typing.Union[MetaOapg.properties.time_updated, None, str, datetime, schemas.Unset] = schemas.unset,
        time_executed: typing.Union[MetaOapg.properties.time_executed, None, str, datetime, schemas.Unset] = schemas.unset,
        expiry_date: typing.Union[MetaOapg.properties.expiry_date, None, str, datetime, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[MetaOapg.additional_properties, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
    ) -> 'AccountOrderRecord':
        return super().__new__(
            cls,
            *args,
            brokerage_order_id=brokerage_order_id,
            status=status,
            symbol=symbol,
            universal_symbol=universal_symbol,
            option_symbol=option_symbol,
            action=action,
            total_quantity=total_quantity,
            open_quantity=open_quantity,
            canceled_quantity=canceled_quantity,
            filled_quantity=filled_quantity,
            execution_price=execution_price,
            limit_price=limit_price,
            stop_price=stop_price,
            order_type=order_type,
            time_in_force=time_in_force,
            time_placed=time_placed,
            time_updated=time_updated,
            time_executed=time_executed,
            expiry_date=expiry_date,
            _configuration=_configuration,
            **kwargs,
        )

from snaptrade_client.model.account_order_record_status import AccountOrderRecordStatus
from snaptrade_client.model.options_symbol import OptionsSymbol
from snaptrade_client.model.universal_symbol import UniversalSymbol
