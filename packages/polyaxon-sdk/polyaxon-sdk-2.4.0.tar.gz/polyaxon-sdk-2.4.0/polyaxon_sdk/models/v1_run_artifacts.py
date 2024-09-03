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


from typing import List, Optional
from pydantic import BaseModel, conlist
from polyaxon_sdk.models.v1_run_artifact import V1RunArtifact

class V1RunArtifacts(BaseModel):
    """
    V1RunArtifacts
    """
    artifacts: Optional[conlist(V1RunArtifact)] = None
    __properties = ["artifacts"]

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
    def from_json(cls, json_str: str) -> V1RunArtifacts:
        """Create an instance of V1RunArtifacts from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in artifacts (list)
        _items = []
        if self.artifacts:
            for _item in self.artifacts:
                if _item:
                    _items.append(_item.to_dict())
            _dict['artifacts'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> V1RunArtifacts:
        """Create an instance of V1RunArtifacts from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return V1RunArtifacts.parse_obj(obj)

        _obj = V1RunArtifacts.parse_obj({
            "artifacts": [V1RunArtifact.from_dict(_item) for _item in obj.get("artifacts")] if obj.get("artifacts") is not None else None
        })
        return _obj

