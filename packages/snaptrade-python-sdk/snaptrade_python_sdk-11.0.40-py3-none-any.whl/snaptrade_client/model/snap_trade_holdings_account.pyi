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


class SnapTradeHoldingsAccount(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)

    SnapTradeUser Investment Account
    """


    class MetaOapg:
        
        class properties:
            id = schemas.UUIDSchema
        
            @staticmethod
            def brokerage_authorization() -> typing.Type['BrokerageAuthorization']:
                return BrokerageAuthorization
            portfolio_group = schemas.UUIDSchema
            
            
            class name(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'name':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            number = schemas.StrSchema
            institution_name = schemas.StrSchema
        
            @staticmethod
            def sync_status() -> typing.Type['AccountSyncStatus']:
                return AccountSyncStatus
        
            @staticmethod
            def meta() -> typing.Type['SnapTradeHoldingsAccountMeta']:
                return SnapTradeHoldingsAccountMeta
            __annotations__ = {
                "id": id,
                "brokerage_authorization": brokerage_authorization,
                "portfolio_group": portfolio_group,
                "name": name,
                "number": number,
                "institution_name": institution_name,
                "sync_status": sync_status,
                "meta": meta,
            }
        additional_properties = schemas.AnyTypeSchema
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["brokerage_authorization"]) -> 'BrokerageAuthorization': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["portfolio_group"]) -> MetaOapg.properties.portfolio_group: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["number"]) -> MetaOapg.properties.number: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["institution_name"]) -> MetaOapg.properties.institution_name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["sync_status"]) -> 'AccountSyncStatus': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["meta"]) -> 'SnapTradeHoldingsAccountMeta': ...
    
    @typing.overload
    def __getitem__(self, name: str) -> MetaOapg.additional_properties: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["id"], typing_extensions.Literal["brokerage_authorization"], typing_extensions.Literal["portfolio_group"], typing_extensions.Literal["name"], typing_extensions.Literal["number"], typing_extensions.Literal["institution_name"], typing_extensions.Literal["sync_status"], typing_extensions.Literal["meta"], str, ]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> typing.Union[MetaOapg.properties.id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["brokerage_authorization"]) -> typing.Union['BrokerageAuthorization', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["portfolio_group"]) -> typing.Union[MetaOapg.properties.portfolio_group, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> typing.Union[MetaOapg.properties.name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["number"]) -> typing.Union[MetaOapg.properties.number, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["institution_name"]) -> typing.Union[MetaOapg.properties.institution_name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["sync_status"]) -> typing.Union['AccountSyncStatus', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["meta"]) -> typing.Union['SnapTradeHoldingsAccountMeta', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[MetaOapg.additional_properties, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["id"], typing_extensions.Literal["brokerage_authorization"], typing_extensions.Literal["portfolio_group"], typing_extensions.Literal["name"], typing_extensions.Literal["number"], typing_extensions.Literal["institution_name"], typing_extensions.Literal["sync_status"], typing_extensions.Literal["meta"], str, ]):
        return super().get_item_oapg(name)

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        brokerage_authorization: typing.Union['BrokerageAuthorization', schemas.Unset] = schemas.unset,
        portfolio_group: typing.Union[MetaOapg.properties.portfolio_group, str, uuid.UUID, schemas.Unset] = schemas.unset,
        name: typing.Union[MetaOapg.properties.name, None, str, schemas.Unset] = schemas.unset,
        number: typing.Union[MetaOapg.properties.number, str, schemas.Unset] = schemas.unset,
        institution_name: typing.Union[MetaOapg.properties.institution_name, str, schemas.Unset] = schemas.unset,
        sync_status: typing.Union['AccountSyncStatus', schemas.Unset] = schemas.unset,
        meta: typing.Union['SnapTradeHoldingsAccountMeta', schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[MetaOapg.additional_properties, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
    ) -> 'SnapTradeHoldingsAccount':
        return super().__new__(
            cls,
            *args,
            id=id,
            brokerage_authorization=brokerage_authorization,
            portfolio_group=portfolio_group,
            name=name,
            number=number,
            institution_name=institution_name,
            sync_status=sync_status,
            meta=meta,
            _configuration=_configuration,
            **kwargs,
        )

from snaptrade_client.model.account_sync_status import AccountSyncStatus
from snaptrade_client.model.brokerage_authorization import BrokerageAuthorization
from snaptrade_client.model.snap_trade_holdings_account_meta import SnapTradeHoldingsAccountMeta
