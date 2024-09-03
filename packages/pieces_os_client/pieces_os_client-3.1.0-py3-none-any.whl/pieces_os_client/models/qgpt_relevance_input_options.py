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
from pieces_os_client.models.qgpt_prompt_pipeline import QGPTPromptPipeline

class QGPTRelevanceInputOptions(BaseModel):
    """
    QGPTRelevanceInputOptions
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    database: Optional[StrictBool] = Field(default=None, description="This is an optional boolen that will tell us to use our entire snippet database as the sample.")
    question: Optional[StrictBool] = Field(default=None, description="This is an optional boolean, that will let the serve know if you want to combine the 2 endpointsboth relevance && the Question endpoint to return the final results.")
    pipeline: Optional[QGPTPromptPipeline] = None
    __properties = ["schema", "database", "question", "pipeline"]

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
    def from_json(cls, json_str: str) -> QGPTRelevanceInputOptions:
        """Create an instance of QGPTRelevanceInputOptions from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of pipeline
        if self.pipeline:
            _dict['pipeline'] = self.pipeline.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> QGPTRelevanceInputOptions:
        """Create an instance of QGPTRelevanceInputOptions from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return QGPTRelevanceInputOptions.parse_obj(obj)

        _obj = QGPTRelevanceInputOptions.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "database": obj.get("database"),
            "question": obj.get("question"),
            "pipeline": QGPTPromptPipeline.from_dict(obj.get("pipeline")) if obj.get("pipeline") is not None else None
        })
        return _obj


