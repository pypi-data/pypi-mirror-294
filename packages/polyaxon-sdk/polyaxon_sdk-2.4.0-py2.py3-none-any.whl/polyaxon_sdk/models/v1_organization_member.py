# coding: utf-8

"""
    Polyaxon SDKs and REST API specification.

         # noqa: E501

    The version of the OpenAPI document: 2.4.0
    Contact: contact@polyaxon.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
from inspect import getfullargspec
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, StrictStr

class V1OrganizationMember(BaseModel):
    """
    V1OrganizationMember
    """
    user: Optional[StrictStr] = None
    user_email: Optional[StrictStr] = None
    role: Optional[StrictStr] = None
    kind: Optional[StrictStr] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    __properties = ["user", "user_email", "role", "kind", "created_at", "updated_at"]

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> V1OrganizationMember:
        """Create an instance of V1OrganizationMember from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> V1OrganizationMember:
        """Create an instance of V1OrganizationMember from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return V1OrganizationMember.parse_obj(obj)

        _obj = V1OrganizationMember.parse_obj({
            "user": obj.get("user"),
            "user_email": obj.get("user_email"),
            "role": obj.get("role"),
            "kind": obj.get("kind"),
            "created_at": obj.get("created_at"),
            "updated_at": obj.get("updated_at")
        })
        return _obj

