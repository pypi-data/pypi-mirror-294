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

from pydantic import BaseModel
from typing import Any, ClassVar, Dict, List
from graphscope.flex.rest.models.create_edge_type import CreateEdgeType
from graphscope.flex.rest.models.create_vertex_type import CreateVertexType
from typing import Optional, Set
from typing_extensions import Self

class CreateGraphSchemaRequest(BaseModel):
    """
    CreateGraphSchemaRequest
    """ # noqa: E501
    vertex_types: List[CreateVertexType]
    edge_types: List[CreateEdgeType]
    __properties: ClassVar[List[str]] = ["vertex_types", "edge_types"]

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
        """Create an instance of CreateGraphSchemaRequest from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in vertex_types (list)
        _items = []
        if self.vertex_types:
            for _item in self.vertex_types:
                if _item:
                    _items.append(_item.to_dict())
            _dict['vertex_types'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in edge_types (list)
        _items = []
        if self.edge_types:
            for _item in self.edge_types:
                if _item:
                    _items.append(_item.to_dict())
            _dict['edge_types'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CreateGraphSchemaRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "vertex_types": [CreateVertexType.from_dict(_item) for _item in obj["vertex_types"]] if obj.get("vertex_types") is not None else None,
            "edge_types": [CreateEdgeType.from_dict(_item) for _item in obj["edge_types"]] if obj.get("edge_types") is not None else None
        })
        return _obj


