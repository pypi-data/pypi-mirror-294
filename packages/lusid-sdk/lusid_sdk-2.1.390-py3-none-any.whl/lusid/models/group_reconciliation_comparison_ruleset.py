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
from pydantic.v1 import BaseModel, Field, StrictStr, conlist, constr
from lusid.models.group_reconciliation_aggregate_attribute_rule import GroupReconciliationAggregateAttributeRule
from lusid.models.group_reconciliation_core_attribute_rule import GroupReconciliationCoreAttributeRule
from lusid.models.link import Link
from lusid.models.resource_id import ResourceId
from lusid.models.version import Version

class GroupReconciliationComparisonRuleset(BaseModel):
    """
    GroupReconciliationComparisonRuleset
    """
    id: ResourceId = Field(...)
    display_name: constr(strict=True, min_length=1) = Field(..., alias="displayName", description="The name of the ruleset")
    reconciliation_type: constr(strict=True, min_length=1) = Field(..., alias="reconciliationType", description="The type of reconciliation to perform. \"Holding\" | \"Transaction\" | \"Valuation\"")
    core_attribute_rules: conlist(GroupReconciliationCoreAttributeRule) = Field(..., alias="coreAttributeRules", description="The core comparison rules")
    aggregate_attribute_rules: conlist(GroupReconciliationAggregateAttributeRule) = Field(..., alias="aggregateAttributeRules", description="The aggregate comparison rules")
    href: Optional[StrictStr] = Field(None, description="The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.")
    version: Optional[Version] = None
    links: Optional[conlist(Link)] = None
    __properties = ["id", "displayName", "reconciliationType", "coreAttributeRules", "aggregateAttributeRules", "href", "version", "links"]

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
    def from_json(cls, json_str: str) -> GroupReconciliationComparisonRuleset:
        """Create an instance of GroupReconciliationComparisonRuleset from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of id
        if self.id:
            _dict['id'] = self.id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in core_attribute_rules (list)
        _items = []
        if self.core_attribute_rules:
            for _item in self.core_attribute_rules:
                if _item:
                    _items.append(_item.to_dict())
            _dict['coreAttributeRules'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in aggregate_attribute_rules (list)
        _items = []
        if self.aggregate_attribute_rules:
            for _item in self.aggregate_attribute_rules:
                if _item:
                    _items.append(_item.to_dict())
            _dict['aggregateAttributeRules'] = _items
        # override the default output from pydantic by calling `to_dict()` of version
        if self.version:
            _dict['version'] = self.version.to_dict()
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

        # set to None if links (nullable) is None
        # and __fields_set__ contains the field
        if self.links is None and "links" in self.__fields_set__:
            _dict['links'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> GroupReconciliationComparisonRuleset:
        """Create an instance of GroupReconciliationComparisonRuleset from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return GroupReconciliationComparisonRuleset.parse_obj(obj)

        _obj = GroupReconciliationComparisonRuleset.parse_obj({
            "id": ResourceId.from_dict(obj.get("id")) if obj.get("id") is not None else None,
            "display_name": obj.get("displayName"),
            "reconciliation_type": obj.get("reconciliationType"),
            "core_attribute_rules": [GroupReconciliationCoreAttributeRule.from_dict(_item) for _item in obj.get("coreAttributeRules")] if obj.get("coreAttributeRules") is not None else None,
            "aggregate_attribute_rules": [GroupReconciliationAggregateAttributeRule.from_dict(_item) for _item in obj.get("aggregateAttributeRules")] if obj.get("aggregateAttributeRules") is not None else None,
            "href": obj.get("href"),
            "version": Version.from_dict(obj.get("version")) if obj.get("version") is not None else None,
            "links": [Link.from_dict(_item) for _item in obj.get("links")] if obj.get("links") is not None else None
        })
        return _obj
