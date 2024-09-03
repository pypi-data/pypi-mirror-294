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
from pydantic import BaseModel, Field, StrictBool
from pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema

class OSDeviceGPUHardwareCapabilitiesInformation(BaseModel):
    """
    This will give specific information on task specific capibilites for GPU.  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    llm: Optional[StrictBool] = Field(default=None, description="This will let us know if in the case we have a gpu and our gpu has the capabilities to use llms")
    __properties = ["schema", "llm"]

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
    def from_json(cls, json_str: str) -> OSDeviceGPUHardwareCapabilitiesInformation:
        """Create an instance of OSDeviceGPUHardwareCapabilitiesInformation from a JSON string"""
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
    def from_dict(cls, obj: dict) -> OSDeviceGPUHardwareCapabilitiesInformation:
        """Create an instance of OSDeviceGPUHardwareCapabilitiesInformation from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return OSDeviceGPUHardwareCapabilitiesInformation.parse_obj(obj)

        _obj = OSDeviceGPUHardwareCapabilitiesInformation.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "llm": obj.get("llm")
        })
        return _obj


