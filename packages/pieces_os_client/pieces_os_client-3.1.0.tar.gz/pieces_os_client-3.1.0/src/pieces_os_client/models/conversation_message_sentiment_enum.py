# coding: utf-8

"""
    Pieces Isomorphic OpenAPI

    Endpoints for Assets, Formats, Users, Asset, Format, User.

    The version of the OpenAPI document: 1.0
    Contact: tsavo@pieces.app
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import json
import pprint
import re  # noqa: F401
from aenum import Enum, no_arg





class ConversationMessageSentimentEnum(str, Enum):
    """
    This will describe the sentiment of a specific message ie if the message was liked/disliked/reported
    """

    """
    allowed enum values
    """
    LIKE = 'LIKE'
    DISLIKE = 'DISLIKE'
    REPORT = 'REPORT'

    @classmethod
    def from_json(cls, json_str: str) -> ConversationMessageSentimentEnum:
        """Create an instance of ConversationMessageSentimentEnum from a JSON string"""
        return ConversationMessageSentimentEnum(json.loads(json_str))


