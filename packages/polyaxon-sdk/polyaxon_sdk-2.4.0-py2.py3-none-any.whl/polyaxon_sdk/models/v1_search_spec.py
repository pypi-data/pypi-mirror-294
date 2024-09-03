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


from typing import Any, Dict, Optional
from pydantic import BaseModel, StrictInt, StrictStr
from polyaxon_sdk.models.v1_analytics_spec import V1AnalyticsSpec
from polyaxon_sdk.models.v1_dashboard_spec import V1DashboardSpec

class V1SearchSpec(BaseModel):
    """
    V1SearchSpec
    """
    query: Optional[StrictStr] = None
    sort: Optional[StrictStr] = None
    limit: Optional[StrictInt] = None
    offset: Optional[StrictInt] = None
    groupby: Optional[StrictStr] = None
    columns: Optional[StrictStr] = None
    layout: Optional[StrictStr] = None
    sections: Optional[StrictStr] = None
    compares: Optional[StrictStr] = None
    heat: Optional[StrictStr] = None
    events: Optional[V1DashboardSpec] = None
    histograms: Optional[Dict[str, Any]] = None
    trends: Optional[Dict[str, Any]] = None
    analytics: Optional[V1AnalyticsSpec] = None
    __properties = ["query", "sort", "limit", "offset", "groupby", "columns", "layout", "sections", "compares", "heat", "events", "histograms", "trends", "analytics"]

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
    def from_json(cls, json_str: str) -> V1SearchSpec:
        """Create an instance of V1SearchSpec from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of events
        if self.events:
            _dict['events'] = self.events.to_dict()
        # override the default output from pydantic by calling `to_dict()` of analytics
        if self.analytics:
            _dict['analytics'] = self.analytics.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> V1SearchSpec:
        """Create an instance of V1SearchSpec from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return V1SearchSpec.parse_obj(obj)

        _obj = V1SearchSpec.parse_obj({
            "query": obj.get("query"),
            "sort": obj.get("sort"),
            "limit": obj.get("limit"),
            "offset": obj.get("offset"),
            "groupby": obj.get("groupby"),
            "columns": obj.get("columns"),
            "layout": obj.get("layout"),
            "sections": obj.get("sections"),
            "compares": obj.get("compares"),
            "heat": obj.get("heat"),
            "events": V1DashboardSpec.from_dict(obj.get("events")) if obj.get("events") is not None else None,
            "histograms": obj.get("histograms"),
            "trends": obj.get("trends"),
            "analytics": V1AnalyticsSpec.from_dict(obj.get("analytics")) if obj.get("analytics") is not None else None
        })
        return _obj

