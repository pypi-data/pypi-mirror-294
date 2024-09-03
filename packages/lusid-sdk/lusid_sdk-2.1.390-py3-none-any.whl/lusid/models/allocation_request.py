# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from pydantic.v1 import BaseModel, Field, StrictFloat, StrictInt, StrictStr, conlist
from lusid.models.currency_and_amount import CurrencyAndAmount
from lusid.models.perpetual_property import PerpetualProperty
from lusid.models.resource_id import ResourceId

class AllocationRequest(BaseModel):
    """
    A request to create or update an Allocation.  # noqa: E501
    """
    properties: Optional[Dict[str, PerpetualProperty]] = Field(None, description="Client-defined properties associated with this allocation.")
    instrument_identifiers: Dict[str, StrictStr] = Field(..., alias="instrumentIdentifiers", description="The instrument allocated.")
    quantity: Union[StrictFloat, StrictInt] = Field(..., description="The quantity of given instrument allocated.")
    portfolio_id: ResourceId = Field(..., alias="portfolioId")
    allocated_order_id: ResourceId = Field(..., alias="allocatedOrderId")
    id: ResourceId = Field(...)
    placement_ids: Optional[conlist(ResourceId)] = Field(None, alias="placementIds", description="A placement - also known as an order placed in the market - associated with this allocation.")
    state: Optional[StrictStr] = Field(None, description="The state of this allocation.")
    side: Optional[StrictStr] = Field(None, description="The side of this allocation (examples: Buy, Sell, ...).")
    type: Optional[StrictStr] = Field(None, description="The type of order associated with this allocation (examples: Limit, Market, ...).")
    settlement_date: Optional[datetime] = Field(None, alias="settlementDate", description="The settlement date for this allocation.")
    var_date: Optional[datetime] = Field(None, alias="date", description="The date of this allocation.")
    price: Optional[CurrencyAndAmount] = None
    settlement_currency: Optional[StrictStr] = Field(None, alias="settlementCurrency", description="The settlement currency of this allocation.")
    settlement_currency_fx_rate: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="settlementCurrencyFxRate", description="The settlement currency to allocation currency FX rate.")
    counterparty: Optional[StrictStr] = Field(None, description="The counterparty for this allocation.")
    execution_ids: Optional[conlist(ResourceId)] = Field(None, alias="executionIds", description="The executions associated with this allocation")
    __properties = ["properties", "instrumentIdentifiers", "quantity", "portfolioId", "allocatedOrderId", "id", "placementIds", "state", "side", "type", "settlementDate", "date", "price", "settlementCurrency", "settlementCurrencyFxRate", "counterparty", "executionIds"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AllocationRequest:
        """Create an instance of AllocationRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each value in properties (dict)
        _field_dict = {}
        if self.properties:
            for _key in self.properties:
                if self.properties[_key]:
                    _field_dict[_key] = self.properties[_key].to_dict()
            _dict['properties'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of portfolio_id
        if self.portfolio_id:
            _dict['portfolioId'] = self.portfolio_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of allocated_order_id
        if self.allocated_order_id:
            _dict['allocatedOrderId'] = self.allocated_order_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of id
        if self.id:
            _dict['id'] = self.id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in placement_ids (list)
        _items = []
        if self.placement_ids:
            for _item in self.placement_ids:
                if _item:
                    _items.append(_item.to_dict())
            _dict['placementIds'] = _items
        # override the default output from pydantic by calling `to_dict()` of price
        if self.price:
            _dict['price'] = self.price.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in execution_ids (list)
        _items = []
        if self.execution_ids:
            for _item in self.execution_ids:
                if _item:
                    _items.append(_item.to_dict())
            _dict['executionIds'] = _items
        # set to None if properties (nullable) is None
        # and __fields_set__ contains the field
        if self.properties is None and "properties" in self.__fields_set__:
            _dict['properties'] = None

        # set to None if placement_ids (nullable) is None
        # and __fields_set__ contains the field
        if self.placement_ids is None and "placement_ids" in self.__fields_set__:
            _dict['placementIds'] = None

        # set to None if state (nullable) is None
        # and __fields_set__ contains the field
        if self.state is None and "state" in self.__fields_set__:
            _dict['state'] = None

        # set to None if side (nullable) is None
        # and __fields_set__ contains the field
        if self.side is None and "side" in self.__fields_set__:
            _dict['side'] = None

        # set to None if type (nullable) is None
        # and __fields_set__ contains the field
        if self.type is None and "type" in self.__fields_set__:
            _dict['type'] = None

        # set to None if settlement_date (nullable) is None
        # and __fields_set__ contains the field
        if self.settlement_date is None and "settlement_date" in self.__fields_set__:
            _dict['settlementDate'] = None

        # set to None if settlement_currency (nullable) is None
        # and __fields_set__ contains the field
        if self.settlement_currency is None and "settlement_currency" in self.__fields_set__:
            _dict['settlementCurrency'] = None

        # set to None if settlement_currency_fx_rate (nullable) is None
        # and __fields_set__ contains the field
        if self.settlement_currency_fx_rate is None and "settlement_currency_fx_rate" in self.__fields_set__:
            _dict['settlementCurrencyFxRate'] = None

        # set to None if counterparty (nullable) is None
        # and __fields_set__ contains the field
        if self.counterparty is None and "counterparty" in self.__fields_set__:
            _dict['counterparty'] = None

        # set to None if execution_ids (nullable) is None
        # and __fields_set__ contains the field
        if self.execution_ids is None and "execution_ids" in self.__fields_set__:
            _dict['executionIds'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AllocationRequest:
        """Create an instance of AllocationRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AllocationRequest.parse_obj(obj)

        _obj = AllocationRequest.parse_obj({
            "properties": dict(
                (_k, PerpetualProperty.from_dict(_v))
                for _k, _v in obj.get("properties").items()
            )
            if obj.get("properties") is not None
            else None,
            "instrument_identifiers": obj.get("instrumentIdentifiers"),
            "quantity": obj.get("quantity"),
            "portfolio_id": ResourceId.from_dict(obj.get("portfolioId")) if obj.get("portfolioId") is not None else None,
            "allocated_order_id": ResourceId.from_dict(obj.get("allocatedOrderId")) if obj.get("allocatedOrderId") is not None else None,
            "id": ResourceId.from_dict(obj.get("id")) if obj.get("id") is not None else None,
            "placement_ids": [ResourceId.from_dict(_item) for _item in obj.get("placementIds")] if obj.get("placementIds") is not None else None,
            "state": obj.get("state"),
            "side": obj.get("side"),
            "type": obj.get("type"),
            "settlement_date": obj.get("settlementDate"),
            "var_date": obj.get("date"),
            "price": CurrencyAndAmount.from_dict(obj.get("price")) if obj.get("price") is not None else None,
            "settlement_currency": obj.get("settlementCurrency"),
            "settlement_currency_fx_rate": obj.get("settlementCurrencyFxRate"),
            "counterparty": obj.get("counterparty"),
            "execution_ids": [ResourceId.from_dict(_item) for _item in obj.get("executionIds")] if obj.get("executionIds") is not None else None
        })
        return _obj
