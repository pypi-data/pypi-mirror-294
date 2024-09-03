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


from typing import Optional
from pydantic import BaseModel
from polyaxon_sdk.models.v1_hp_choice import V1HpChoice
from polyaxon_sdk.models.v1_hp_date_range import V1HpDateRange
from polyaxon_sdk.models.v1_hp_date_time_range import V1HpDateTimeRange
from polyaxon_sdk.models.v1_hp_geom_space import V1HpGeomSpace
from polyaxon_sdk.models.v1_hp_lin_space import V1HpLinSpace
from polyaxon_sdk.models.v1_hp_log_normal import V1HpLogNormal
from polyaxon_sdk.models.v1_hp_log_space import V1HpLogSpace
from polyaxon_sdk.models.v1_hp_log_uniform import V1HpLogUniform
from polyaxon_sdk.models.v1_hp_normal import V1HpNormal
from polyaxon_sdk.models.v1_hp_p_choice import V1HpPChoice
from polyaxon_sdk.models.v1_hp_q_log_normal import V1HpQLogNormal
from polyaxon_sdk.models.v1_hp_q_log_uniform import V1HpQLogUniform
from polyaxon_sdk.models.v1_hp_q_normal import V1HpQNormal
from polyaxon_sdk.models.v1_hp_q_uniform import V1HpQUniform
from polyaxon_sdk.models.v1_hp_range import V1HpRange
from polyaxon_sdk.models.v1_hp_uniform import V1HpUniform

class V1HpParams(BaseModel):
    """
    V1HpParams
    """
    choice: Optional[V1HpChoice] = None
    pchoice: Optional[V1HpPChoice] = None
    range: Optional[V1HpRange] = None
    linspace: Optional[V1HpLinSpace] = None
    logspace: Optional[V1HpLogSpace] = None
    geomspace: Optional[V1HpGeomSpace] = None
    uniform: Optional[V1HpUniform] = None
    quniform: Optional[V1HpQUniform] = None
    loguniform: Optional[V1HpLogUniform] = None
    qloguniform: Optional[V1HpQLogUniform] = None
    normal: Optional[V1HpNormal] = None
    qnormal: Optional[V1HpQNormal] = None
    lognormal: Optional[V1HpLogNormal] = None
    qlognormal: Optional[V1HpQLogNormal] = None
    daterange: Optional[V1HpDateRange] = None
    datetimerange: Optional[V1HpDateTimeRange] = None
    __properties = ["choice", "pchoice", "range", "linspace", "logspace", "geomspace", "uniform", "quniform", "loguniform", "qloguniform", "normal", "qnormal", "lognormal", "qlognormal", "daterange", "datetimerange"]

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
    def from_json(cls, json_str: str) -> V1HpParams:
        """Create an instance of V1HpParams from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of choice
        if self.choice:
            _dict['choice'] = self.choice.to_dict()
        # override the default output from pydantic by calling `to_dict()` of pchoice
        if self.pchoice:
            _dict['pchoice'] = self.pchoice.to_dict()
        # override the default output from pydantic by calling `to_dict()` of range
        if self.range:
            _dict['range'] = self.range.to_dict()
        # override the default output from pydantic by calling `to_dict()` of linspace
        if self.linspace:
            _dict['linspace'] = self.linspace.to_dict()
        # override the default output from pydantic by calling `to_dict()` of logspace
        if self.logspace:
            _dict['logspace'] = self.logspace.to_dict()
        # override the default output from pydantic by calling `to_dict()` of geomspace
        if self.geomspace:
            _dict['geomspace'] = self.geomspace.to_dict()
        # override the default output from pydantic by calling `to_dict()` of uniform
        if self.uniform:
            _dict['uniform'] = self.uniform.to_dict()
        # override the default output from pydantic by calling `to_dict()` of quniform
        if self.quniform:
            _dict['quniform'] = self.quniform.to_dict()
        # override the default output from pydantic by calling `to_dict()` of loguniform
        if self.loguniform:
            _dict['loguniform'] = self.loguniform.to_dict()
        # override the default output from pydantic by calling `to_dict()` of qloguniform
        if self.qloguniform:
            _dict['qloguniform'] = self.qloguniform.to_dict()
        # override the default output from pydantic by calling `to_dict()` of normal
        if self.normal:
            _dict['normal'] = self.normal.to_dict()
        # override the default output from pydantic by calling `to_dict()` of qnormal
        if self.qnormal:
            _dict['qnormal'] = self.qnormal.to_dict()
        # override the default output from pydantic by calling `to_dict()` of lognormal
        if self.lognormal:
            _dict['lognormal'] = self.lognormal.to_dict()
        # override the default output from pydantic by calling `to_dict()` of qlognormal
        if self.qlognormal:
            _dict['qlognormal'] = self.qlognormal.to_dict()
        # override the default output from pydantic by calling `to_dict()` of daterange
        if self.daterange:
            _dict['daterange'] = self.daterange.to_dict()
        # override the default output from pydantic by calling `to_dict()` of datetimerange
        if self.datetimerange:
            _dict['datetimerange'] = self.datetimerange.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> V1HpParams:
        """Create an instance of V1HpParams from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return V1HpParams.parse_obj(obj)

        _obj = V1HpParams.parse_obj({
            "choice": V1HpChoice.from_dict(obj.get("choice")) if obj.get("choice") is not None else None,
            "pchoice": V1HpPChoice.from_dict(obj.get("pchoice")) if obj.get("pchoice") is not None else None,
            "range": V1HpRange.from_dict(obj.get("range")) if obj.get("range") is not None else None,
            "linspace": V1HpLinSpace.from_dict(obj.get("linspace")) if obj.get("linspace") is not None else None,
            "logspace": V1HpLogSpace.from_dict(obj.get("logspace")) if obj.get("logspace") is not None else None,
            "geomspace": V1HpGeomSpace.from_dict(obj.get("geomspace")) if obj.get("geomspace") is not None else None,
            "uniform": V1HpUniform.from_dict(obj.get("uniform")) if obj.get("uniform") is not None else None,
            "quniform": V1HpQUniform.from_dict(obj.get("quniform")) if obj.get("quniform") is not None else None,
            "loguniform": V1HpLogUniform.from_dict(obj.get("loguniform")) if obj.get("loguniform") is not None else None,
            "qloguniform": V1HpQLogUniform.from_dict(obj.get("qloguniform")) if obj.get("qloguniform") is not None else None,
            "normal": V1HpNormal.from_dict(obj.get("normal")) if obj.get("normal") is not None else None,
            "qnormal": V1HpQNormal.from_dict(obj.get("qnormal")) if obj.get("qnormal") is not None else None,
            "lognormal": V1HpLogNormal.from_dict(obj.get("lognormal")) if obj.get("lognormal") is not None else None,
            "qlognormal": V1HpQLogNormal.from_dict(obj.get("qlognormal")) if obj.get("qlognormal") is not None else None,
            "daterange": V1HpDateRange.from_dict(obj.get("daterange")) if obj.get("daterange") is not None else None,
            "datetimerange": V1HpDateTimeRange.from_dict(obj.get("datetimerange")) if obj.get("datetimerange") is not None else None
        })
        return _obj

