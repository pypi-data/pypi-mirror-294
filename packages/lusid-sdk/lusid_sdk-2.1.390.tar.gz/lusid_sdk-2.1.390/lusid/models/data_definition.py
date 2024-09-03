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
from pydantic.v1 import BaseModel, Field, StrictBool, StrictStr, constr, validator

class DataDefinition(BaseModel):
    """
    When importing data from an external data source, in order for it to be reliable queryable, LUSID needs to know something about it.  A data definition tells LUSID, what a given external data item is, what type it is and whether it in some way identifies items of data.  Consider presenting LUSID with a list of dictionaries where each dictionary contains the same set of keys (names). Each data item pointed to by  a key would be expected to be of the same type (integer, string, decimal etc.). To identify a particular dictionary from the list, a tuple of  one or more of the items in the dictionary would make it unique. If only a single item is required then the  # noqa: E501
    """
    address: StrictStr = Field(..., description="The internal address (LUSID native) of the unit in the provided data itself and corresponds to the external name of the data item")
    name: Optional[constr(strict=True, max_length=256, min_length=1)] = Field(None, description="The name of the data item. This is the name that will appear")
    data_type: Optional[constr(strict=True, max_length=128, min_length=0)] = Field(None, alias="dataType", description="A member of the set of possible data types, that all data passed under that key is expected to be of.  Currently limited to one of [string, integer, decimal, result0d].")
    key_type: Optional[constr(strict=True, max_length=128, min_length=0)] = Field(None, alias="keyType", description="Is the item either a unique key for the dictionary, i.e. does it identify a unique index or conceptual 'row' within the list of dictionaries,  or a partial key or is it simply a data item within that dictionary. Must be one of [Unique,PartOfUnique,Leaf, CompositeLeaf]")
    allow_null: Optional[StrictBool] = Field(None, alias="allowNull", description="The path to the field must exist (unless AllowMissing is true) but the actual value is allowed to be null.")
    allow_missing: Optional[StrictBool] = Field(None, alias="allowMissing", description="The path (or column) is allowed to be missing but if it is present it is not allowed to be null unless AllowNull is true.")
    __properties = ["address", "name", "dataType", "keyType", "allowNull", "allowMissing"]

    @validator('name')
    def name_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r"^[a-zA-Z0-9\-_]+$", value):
            raise ValueError(r"must validate the regular expression /^[a-zA-Z0-9\-_]+$/")
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
    def from_json(cls, json_str: str) -> DataDefinition:
        """Create an instance of DataDefinition from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if name (nullable) is None
        # and __fields_set__ contains the field
        if self.name is None and "name" in self.__fields_set__:
            _dict['name'] = None

        # set to None if data_type (nullable) is None
        # and __fields_set__ contains the field
        if self.data_type is None and "data_type" in self.__fields_set__:
            _dict['dataType'] = None

        # set to None if key_type (nullable) is None
        # and __fields_set__ contains the field
        if self.key_type is None and "key_type" in self.__fields_set__:
            _dict['keyType'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DataDefinition:
        """Create an instance of DataDefinition from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DataDefinition.parse_obj(obj)

        _obj = DataDefinition.parse_obj({
            "address": obj.get("address"),
            "name": obj.get("name"),
            "data_type": obj.get("dataType"),
            "key_type": obj.get("keyType"),
            "allow_null": obj.get("allowNull"),
            "allow_missing": obj.get("allowMissing")
        })
        return _obj
