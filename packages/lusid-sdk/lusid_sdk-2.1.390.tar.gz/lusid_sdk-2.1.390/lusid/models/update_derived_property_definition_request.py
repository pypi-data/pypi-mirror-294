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


from typing import Any, Dict, Optional
from pydantic.v1 import BaseModel, Field, constr
from lusid.models.resource_id import ResourceId

class UpdateDerivedPropertyDefinitionRequest(BaseModel):
    """
    UpdateDerivedPropertyDefinitionRequest
    """
    display_name: constr(strict=True, min_length=1) = Field(..., alias="displayName", description="The display name of the property.")
    data_type_id: ResourceId = Field(..., alias="dataTypeId")
    property_description: Optional[constr(strict=True, max_length=512)] = Field(None, alias="propertyDescription", description="Describes the property")
    derivation_formula: constr(strict=True, min_length=1) = Field(..., alias="derivationFormula", description="The rule that defines how data is composed for a derived property.")
    __properties = ["displayName", "dataTypeId", "propertyDescription", "derivationFormula"]

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
    def from_json(cls, json_str: str) -> UpdateDerivedPropertyDefinitionRequest:
        """Create an instance of UpdateDerivedPropertyDefinitionRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of data_type_id
        if self.data_type_id:
            _dict['dataTypeId'] = self.data_type_id.to_dict()
        # set to None if property_description (nullable) is None
        # and __fields_set__ contains the field
        if self.property_description is None and "property_description" in self.__fields_set__:
            _dict['propertyDescription'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> UpdateDerivedPropertyDefinitionRequest:
        """Create an instance of UpdateDerivedPropertyDefinitionRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return UpdateDerivedPropertyDefinitionRequest.parse_obj(obj)

        _obj = UpdateDerivedPropertyDefinitionRequest.parse_obj({
            "display_name": obj.get("displayName"),
            "data_type_id": ResourceId.from_dict(obj.get("dataTypeId")) if obj.get("dataTypeId") is not None else None,
            "property_description": obj.get("propertyDescription"),
            "derivation_formula": obj.get("derivationFormula")
        })
        return _obj
