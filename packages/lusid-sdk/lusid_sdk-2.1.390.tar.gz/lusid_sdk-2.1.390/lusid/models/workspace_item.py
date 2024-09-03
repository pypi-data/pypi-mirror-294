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
from pydantic.v1 import BaseModel, Field, StrictInt, conlist, constr, validator
from lusid.models.link import Link
from lusid.models.version import Version

class WorkspaceItem(BaseModel):
    """
    An item stored in a workspace.  # noqa: E501
    """
    type: constr(strict=True, min_length=1) = Field(..., description="The type of the workspace item.")
    format: StrictInt = Field(..., description="A simple integer format identifier.")
    name: constr(strict=True, min_length=1) = Field(..., description="A workspace item's name; a unique identifier.")
    description: constr(strict=True, max_length=1024, min_length=0) = Field(..., description="The description of a workspace item.")
    content: constr(strict=True, max_length=6000, min_length=0) = Field(..., description="The content associated with a workspace item.")
    version: Optional[Version] = None
    links: Optional[conlist(Link)] = None
    __properties = ["type", "format", "name", "description", "content", "version", "links"]

    @validator('description')
    def description_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[\s\S]*$", value):
            raise ValueError(r"must validate the regular expression /^[\s\S]*$/")
        return value

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
    def from_json(cls, json_str: str) -> WorkspaceItem:
        """Create an instance of WorkspaceItem from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in links (list)
        _items = []
        if self.links:
            for _item in self.links:
                if _item:
                    _items.append(_item.to_dict())
            _dict['links'] = _items
        # set to None if links (nullable) is None
        # and __fields_set__ contains the field
        if self.links is None and "links" in self.__fields_set__:
            _dict['links'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> WorkspaceItem:
        """Create an instance of WorkspaceItem from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return WorkspaceItem.parse_obj(obj)

        _obj = WorkspaceItem.parse_obj({
            "type": obj.get("type"),
            "format": obj.get("format"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "content": obj.get("content"),
            "version": Version.from_dict(obj.get("version")) if obj.get("version") is not None else None,
            "links": [Link.from_dict(_item) for _item in obj.get("links")] if obj.get("links") is not None else None
        })
        return _obj
