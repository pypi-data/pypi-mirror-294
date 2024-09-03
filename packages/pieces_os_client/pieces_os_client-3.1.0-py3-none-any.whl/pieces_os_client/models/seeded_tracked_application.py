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
from pydantic import BaseModel, Field, StrictBool, StrictStr
from pieces_os_client.models.application_name_enum import ApplicationNameEnum
from pieces_os_client.models.capabilities_enum import CapabilitiesEnum
from pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from pieces_os_client.models.platform_enum import PlatformEnum
from pieces_os_client.models.privacy_enum import PrivacyEnum

class SeededTrackedApplication(BaseModel):
    """
      # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    name: ApplicationNameEnum = Field(...)
    version: StrictStr = Field(default=..., description="This is the specific version number 0.0.0")
    platform: PlatformEnum = Field(...)
    capabilities: Optional[CapabilitiesEnum] = None
    privacy: Optional[PrivacyEnum] = None
    automatic_unload: Optional[StrictBool] = Field(default=None, alias="automaticUnload", description="This is a proper that will let us know if we will proactivity unload all of your machine learning models.by default this is false.")
    __properties = ["schema", "name", "version", "platform", "capabilities", "privacy", "automaticUnload"]

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
    def from_json(cls, json_str: str) -> SeededTrackedApplication:
        """Create an instance of SeededTrackedApplication from a JSON string"""
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
    def from_dict(cls, obj: dict) -> SeededTrackedApplication:
        """Create an instance of SeededTrackedApplication from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SeededTrackedApplication.parse_obj(obj)

        _obj = SeededTrackedApplication.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "name": obj.get("name"),
            "version": obj.get("version"),
            "platform": obj.get("platform"),
            "capabilities": obj.get("capabilities"),
            "privacy": obj.get("privacy"),
            "automatic_unload": obj.get("automaticUnload")
        })
        return _obj


