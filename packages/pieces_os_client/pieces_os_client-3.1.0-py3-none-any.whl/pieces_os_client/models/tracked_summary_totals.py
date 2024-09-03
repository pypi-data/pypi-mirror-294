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



from pydantic import BaseModel, Field, StrictInt

class TrackedSummaryTotals(BaseModel):
    """
    This is the counts of things that users can add.  # noqa: E501
    """
    assets: StrictInt = Field(...)
    tags: StrictInt = Field(...)
    websites: StrictInt = Field(...)
    persons: StrictInt = Field(...)
    sensitives: StrictInt = Field(...)
    shares: StrictInt = Field(...)
    copilot_sends: StrictInt = Field(...)
    copilot_receives: StrictInt = Field(...)
    copilot_sessions: StrictInt = Field(...)
    copilot_conversations: StrictInt = Field(...)
    productivity_score: StrictInt = Field(...)
    searches: StrictInt = Field(...)
    references: StrictInt = Field(...)
    reuses: StrictInt = Field(...)
    anchor_files: StrictInt = Field(...)
    anchor_folders: StrictInt = Field(...)
    isr_reports: StrictInt = Field(...)
    __properties = ["assets", "tags", "websites", "persons", "sensitives", "shares", "copilot_sends", "copilot_receives", "copilot_sessions", "copilot_conversations", "productivity_score", "searches", "references", "reuses", "anchor_files", "anchor_folders", "isr_reports"]

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
    def from_json(cls, json_str: str) -> TrackedSummaryTotals:
        """Create an instance of TrackedSummaryTotals from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TrackedSummaryTotals:
        """Create an instance of TrackedSummaryTotals from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TrackedSummaryTotals.parse_obj(obj)

        _obj = TrackedSummaryTotals.parse_obj({
            "assets": obj.get("assets"),
            "tags": obj.get("tags"),
            "websites": obj.get("websites"),
            "persons": obj.get("persons"),
            "sensitives": obj.get("sensitives"),
            "shares": obj.get("shares"),
            "copilot_sends": obj.get("copilot_sends"),
            "copilot_receives": obj.get("copilot_receives"),
            "copilot_sessions": obj.get("copilot_sessions"),
            "copilot_conversations": obj.get("copilot_conversations"),
            "productivity_score": obj.get("productivity_score"),
            "searches": obj.get("searches"),
            "references": obj.get("references"),
            "reuses": obj.get("reuses"),
            "anchor_files": obj.get("anchor_files"),
            "anchor_folders": obj.get("anchor_folders"),
            "isr_reports": obj.get("isr_reports")
        })
        return _obj


