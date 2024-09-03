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


from typing import Any, Dict
from pydantic.v1 import BaseModel, Field, StrictStr

class DeleteRelationRequest(BaseModel):
    """
    DeleteRelationRequest
    """
    source_entity_id: Dict[str, StrictStr] = Field(..., alias="sourceEntityId", description="The identifier of the source entity of the relation to be deleted.")
    target_entity_id: Dict[str, StrictStr] = Field(..., alias="targetEntityId", description="The identifier of the target entity of the relation to be deleted.")
    __properties = ["sourceEntityId", "targetEntityId"]

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
    def from_json(cls, json_str: str) -> DeleteRelationRequest:
        """Create an instance of DeleteRelationRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DeleteRelationRequest:
        """Create an instance of DeleteRelationRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DeleteRelationRequest.parse_obj(obj)

        _obj = DeleteRelationRequest.parse_obj({
            "source_entity_id": obj.get("sourceEntityId"),
            "target_entity_id": obj.get("targetEntityId")
        })
        return _obj
