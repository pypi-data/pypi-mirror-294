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


from typing import Any, Dict, Union
from pydantic.v1 import BaseModel, Field, StrictStr, validator
import lusid.models

class ComplianceStep(BaseModel):
    """
    ComplianceStep
    """
    compliance_step_type: StrictStr = Field(..., alias="complianceStepType", description=". The available values are: FilterStep, GroupByStep, GroupFilterStep, BranchStep, RecombineStep, CheckStep, PercentCheckStep")
    __properties = ["complianceStepType"]

    @validator('compliance_step_type')
    def compliance_step_type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('FilterStep', 'GroupByStep', 'GroupFilterStep', 'BranchStep', 'RecombineStep', 'CheckStep', 'PercentCheckStep'):
            raise ValueError("must be one of enum values ('FilterStep', 'GroupByStep', 'GroupFilterStep', 'BranchStep', 'RecombineStep', 'CheckStep', 'PercentCheckStep')")
        return value

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    # JSON field name that stores the object type
    __discriminator_property_name = 'complianceStepType'

    # discriminator mappings
    __discriminator_value_class_map = {
        'BranchStep': 'BranchStep',
        'CheckStep': 'CheckStep',
        'FilterStep': 'FilterStep',
        'GroupByStep': 'GroupByStep',
        'GroupFilterStep': 'GroupFilterStep',
        'IntermediateComplianceStep': 'IntermediateComplianceStep',
        'PercentCheckStep': 'PercentCheckStep',
        'RecombineStep': 'RecombineStep'
    }

    @classmethod
    def get_discriminator_value(cls, obj: dict) -> str:
        """Returns the discriminator value (object type) of the data"""
        discriminator_value = obj[cls.__discriminator_property_name]
        if discriminator_value:
            return cls.__discriminator_value_class_map.get(discriminator_value)
        else:
            return None

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Union(BranchStep, CheckStep, FilterStep, GroupByStep, GroupFilterStep, IntermediateComplianceStep, PercentCheckStep, RecombineStep):
        """Create an instance of ComplianceStep from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Union(BranchStep, CheckStep, FilterStep, GroupByStep, GroupFilterStep, IntermediateComplianceStep, PercentCheckStep, RecombineStep):
        """Create an instance of ComplianceStep from a dict"""
        # look up the object type based on discriminator mapping
        object_type = cls.get_discriminator_value(obj)
        if object_type:
            klass = getattr(lusid.models, object_type)
            return klass.from_dict(obj)
        else:
            raise ValueError("ComplianceStep failed to lookup discriminator value from " +
                             json.dumps(obj) + ". Discriminator property name: " + cls.__discriminator_property_name +
                             ", mapping: " + json.dumps(cls.__discriminator_value_class_map))
