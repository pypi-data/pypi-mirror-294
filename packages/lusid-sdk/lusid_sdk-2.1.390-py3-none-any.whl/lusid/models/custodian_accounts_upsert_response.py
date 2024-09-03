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


from typing import Any, Dict, List, Optional
from pydantic.v1 import BaseModel, Field, StrictStr, conlist
from lusid.models.custodian_account import CustodianAccount
from lusid.models.link import Link
from lusid.models.version import Version

class CustodianAccountsUpsertResponse(BaseModel):
    """
    The upsert accounts response  # noqa: E501
    """
    href: Optional[StrictStr] = Field(None, description="The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.")
    version: Optional[Version] = None
    custodian_accounts: Optional[conlist(CustodianAccount)] = Field(None, alias="custodianAccounts", description="The Custodian Accounts which have been upserted.")
    links: Optional[conlist(Link)] = None
    __properties = ["href", "version", "custodianAccounts", "links"]

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
    def from_json(cls, json_str: str) -> CustodianAccountsUpsertResponse:
        """Create an instance of CustodianAccountsUpsertResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of version
        if self.version:
            _dict['version'] = self.version.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in custodian_accounts (list)
        _items = []
        if self.custodian_accounts:
            for _item in self.custodian_accounts:
                if _item:
                    _items.append(_item.to_dict())
            _dict['custodianAccounts'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in links (list)
        _items = []
        if self.links:
            for _item in self.links:
                if _item:
                    _items.append(_item.to_dict())
            _dict['links'] = _items
        # set to None if href (nullable) is None
        # and __fields_set__ contains the field
        if self.href is None and "href" in self.__fields_set__:
            _dict['href'] = None

        # set to None if custodian_accounts (nullable) is None
        # and __fields_set__ contains the field
        if self.custodian_accounts is None and "custodian_accounts" in self.__fields_set__:
            _dict['custodianAccounts'] = None

        # set to None if links (nullable) is None
        # and __fields_set__ contains the field
        if self.links is None and "links" in self.__fields_set__:
            _dict['links'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CustodianAccountsUpsertResponse:
        """Create an instance of CustodianAccountsUpsertResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CustodianAccountsUpsertResponse.parse_obj(obj)

        _obj = CustodianAccountsUpsertResponse.parse_obj({
            "href": obj.get("href"),
            "version": Version.from_dict(obj.get("version")) if obj.get("version") is not None else None,
            "custodian_accounts": [CustodianAccount.from_dict(_item) for _item in obj.get("custodianAccounts")] if obj.get("custodianAccounts") is not None else None,
            "links": [Link.from_dict(_item) for _item in obj.get("links")] if obj.get("links") is not None else None
        })
        return _obj
