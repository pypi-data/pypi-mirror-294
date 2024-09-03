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
from pieces_os_client.models.grouped_timestamp import GroupedTimestamp
from pieces_os_client.models.referenced_workstream_summary import ReferencedWorkstreamSummary
from pieces_os_client.models.seeded_range_conversation_association import SeededRangeConversationAssociation

class SeededRange(BaseModel):
    """
    This is a preIdentified version of a Range.  conversation: this is here to specify the relationship that we want to set up with the Range.  IE for this case we want to associate a Range with a Conversation.grounding.temporal.workstream. Otherwise, if this was a conversation we would have no way to know what relationship that we want to set up on the conversation w/ the range. (because this will be set up for many relationShip opportunities that have different functionalities)  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    to: Optional[GroupedTimestamp] = None
    var_from: Optional[GroupedTimestamp] = Field(default=None, alias="from")
    between: Optional[StrictBool] = None
    summary: Optional[ReferencedWorkstreamSummary] = None
    conversation: Optional[SeededRangeConversationAssociation] = None
    __properties = ["schema", "to", "from", "between", "summary", "conversation"]

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
    def from_json(cls, json_str: str) -> SeededRange:
        """Create an instance of SeededRange from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of to
        if self.to:
            _dict['to'] = self.to.to_dict()
        # override the default output from pydantic by calling `to_dict()` of var_from
        if self.var_from:
            _dict['from'] = self.var_from.to_dict()
        # override the default output from pydantic by calling `to_dict()` of summary
        if self.summary:
            _dict['summary'] = self.summary.to_dict()
        # override the default output from pydantic by calling `to_dict()` of conversation
        if self.conversation:
            _dict['conversation'] = self.conversation.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SeededRange:
        """Create an instance of SeededRange from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SeededRange.parse_obj(obj)

        _obj = SeededRange.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "to": GroupedTimestamp.from_dict(obj.get("to")) if obj.get("to") is not None else None,
            "var_from": GroupedTimestamp.from_dict(obj.get("from")) if obj.get("from") is not None else None,
            "between": obj.get("between"),
            "summary": ReferencedWorkstreamSummary.from_dict(obj.get("summary")) if obj.get("summary") is not None else None,
            "conversation": SeededRangeConversationAssociation.from_dict(obj.get("conversation")) if obj.get("conversation") is not None else None
        })
        return _obj


