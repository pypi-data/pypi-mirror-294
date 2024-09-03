# coding: utf-8

"""
    GraphScope FLEX HTTP SERVICE API

    This is a specification for GraphScope FLEX HTTP service based on the OpenAPI 3.0 specification. You can find out more details about specification at [doc](https://swagger.io/specification/v3/).  Some useful links: - [GraphScope Repository](https://github.com/alibaba/GraphScope) - [The Source API definition for GraphScope Interactive](https://github.com/GraphScope/portal/tree/main/httpservice)

    The version of the OpenAPI document: 1.0.0
    Contact: graphscope@alibaba-inc.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from graphscope.flex.rest.models.base_vertex_type_x_csr_params import BaseVertexTypeXCsrParams
from graphscope.flex.rest.models.get_property_meta import GetPropertyMeta
from typing import Optional, Set
from typing_extensions import Self

class GetVertexType(BaseModel):
    """
    GetVertexType
    """ # noqa: E501
    type_name: StrictStr
    primary_keys: List[StrictStr]
    x_csr_params: Optional[BaseVertexTypeXCsrParams] = None
    type_id: Optional[StrictInt] = None
    properties: List[GetPropertyMeta]
    description: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = ["type_name", "primary_keys", "x_csr_params", "type_id", "properties", "description"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of GetVertexType from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of x_csr_params
        if self.x_csr_params:
            _dict['x_csr_params'] = self.x_csr_params.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in properties (list)
        _items = []
        if self.properties:
            for _item in self.properties:
                if _item:
                    _items.append(_item.to_dict())
            _dict['properties'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of GetVertexType from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "type_name": obj.get("type_name"),
            "primary_keys": obj.get("primary_keys"),
            "x_csr_params": BaseVertexTypeXCsrParams.from_dict(obj["x_csr_params"]) if obj.get("x_csr_params") is not None else None,
            "type_id": obj.get("type_id"),
            "properties": [GetPropertyMeta.from_dict(_item) for _item in obj["properties"]] if obj.get("properties") is not None else None,
            "description": obj.get("description")
        })
        return _obj


