# coding: utf-8

"""
    Pieces Isomorphic OpenAPI

    Endpoints for Assets, Formats, Users, Asset, Format, User.

    The version of the OpenAPI document: 1.0
    Contact: tsavo@pieces.app
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Optional
from pydantic import BaseModel, Field, StrictStr
from pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from pieces_os_client.models.mechanism_enum import MechanismEnum
from pieces_os_client.models.tag_category_enum import TagCategoryEnum

class SeededTag(BaseModel):
    """
    This is the minimum information needed when creating a Tag.  Default we will attach manual to a tag unless otherwise specified for mechanism.  you can optionally add an asset, format, or person uuid to attach this tag directly to it  TODO consider updating these asset,format to referenced Models  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    text: StrictStr = Field(default=..., description="This is the description of the tag.")
    asset: Optional[StrictStr] = Field(default=None, description="this is a uuid that references an asset.")
    mechanism: Optional[MechanismEnum] = None
    category: Optional[TagCategoryEnum] = None
    person: Optional[StrictStr] = Field(default=None, description="uuid of the person, you want to add this tag too")
    __properties = ["schema", "text", "asset", "mechanism", "category", "person"]

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
    def from_json(cls, json_str: str) -> SeededTag:
        """Create an instance of SeededTag from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of var_schema
        if self.var_schema:
            _dict['schema'] = self.var_schema.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SeededTag:
        """Create an instance of SeededTag from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SeededTag.parse_obj(obj)

        _obj = SeededTag.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "text": obj.get("text"),
            "asset": obj.get("asset"),
            "mechanism": obj.get("mechanism"),
            "category": obj.get("category"),
            "person": obj.get("person")
        })
        return _obj


