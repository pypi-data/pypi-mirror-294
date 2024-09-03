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
from pydantic import BaseModel, Field, StrictStr, validator
from pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema

class ChallengedPKCE(BaseModel):
    """
    A model that Generates A PKCE Challenge Object with the needed requirements.  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    state: StrictStr = Field(default=..., description="An opaque value the clients adds to the initial request that Auth0 includes when redirecting the back to the client. This value must be used by the client to prevent CSRF attacks.")
    nonce: StrictStr = Field(default=..., description="A local key that is held as the comparator to state, thus they should be the same.")
    challenge: StrictStr = Field(default=..., description="Generated challenge from the code_verifier.")
    method: StrictStr = Field(default=..., description="Method used to generate the challenge. The PKCE spec defines two methods, S256 and plain, however, Auth0 supports only S256 since the latter is discouraged.")
    verifier: StrictStr = Field(default=..., description="Cryptographically random key that was used to generate the code_challenge passed to /authorize.")
    __properties = ["schema", "state", "nonce", "challenge", "method", "verifier"]

    @validator('method')
    def method_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('S256'):
            raise ValueError("must be one of enum values ('S256')")
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
    def from_json(cls, json_str: str) -> ChallengedPKCE:
        """Create an instance of ChallengedPKCE from a JSON string"""
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
    def from_dict(cls, obj: dict) -> ChallengedPKCE:
        """Create an instance of ChallengedPKCE from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ChallengedPKCE.parse_obj(obj)

        _obj = ChallengedPKCE.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "state": obj.get("state"),
            "nonce": obj.get("nonce"),
            "challenge": obj.get("challenge"),
            "method": obj.get("method"),
            "verifier": obj.get("verifier")
        })
        return _obj


