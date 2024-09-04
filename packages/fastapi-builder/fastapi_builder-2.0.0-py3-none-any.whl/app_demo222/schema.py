import datetime
from typing import List, Literal

from fastapi import Query
from pydantic import Field, field_validator
from apps.app_it_demo1.field import Demo222Fields
from apps.app_it_demo1.model import Demo222
from models.base import get_model_fields_from_objects
from schemas.base import BaseSchema, QuerySchema
from schemas.response import PaginationResponse, StandardResponse


# ======================>>>>>>>>>>>>>>>>>>>>>> get_it_demos


class Demo222ListQueryRequest(QuerySchema):
    """获取 it_demo1 列表 查询 请求"""

    order_by: Literal["id", "created_at"] = Query(
        Demo222.id.name, description="排序字段. eg: id created_at"
    )

    @field_validator("order_by")
    def validate_order_by(cls, v: str) -> str:
        order_fields = get_model_fields_from_objects(Demo222, [Demo222.id, Demo222.created_at])
        if v not in order_fields:
            raise ValueError(f"order_by: {v} not in {order_fields}")
        return v


class Demo222ListResponse(BaseSchema):
    """获取 it_demo1 列表 响应"""

    id: int = Demo222Fields.id
    name: str = Demo222Fields.name


class Demo222ListResponseModel(StandardResponse):
    """获取 it_demo1 列表 响应 Model"""

    data: PaginationResponse[Demo222ListResponse]


# ======================>>>>>>>>>>>>>>>>>>>>>> create_it_demo1


class Demo222CreateRequest(BaseSchema):
    """创建 it_demo1 请求"""

    name: str = Demo222Fields.name


class Demo222CreateResponse(BaseSchema):
    """创建 it_demo1 响应"""

    id: int = Demo222Fields.id
    name: str = Demo222Fields.name


class Demo222CreateResponseModel(StandardResponse):
    """创建 it_demo1 响应 Model"""

    data: Demo222CreateResponse | None = None


# ======================>>>>>>>>>>>>>>>>>>>>>> patch_it_demo1s


class Demo222sPatchRequest(BaseSchema):
    """批量更新 it_demo1 请求"""

    ids: List[int] = Field(..., description="it_demo1 id 列表")
    name: str = Demo222Fields.name


class Demo222sPatchResponse(BaseSchema):
    """批量更新 it_demo1 响应"""

    ids: List[int] = Field(..., description="it_demo1 id 列表")
    name: str = Demo222Fields.name


class Demo222sPatchResponseModel(StandardResponse):
    """批量更新 it_demo1 响应 Model"""

    data: Demo222sPatchResponse | None = None


# ======================>>>>>>>>>>>>>>>>>>>>>> delete_it_demo1s


class Demo222sDeleteResponse(BaseSchema):
    """批量删除 it_demo1 响应"""

    ids: List[int] = Field(..., description="it_demo1 id 列表")


class Demo222sDeleteResponseModel(StandardResponse):
    """批量删除 it_demo1 响应 Model"""

    data: Demo222sDeleteResponse


# ======================>>>>>>>>>>>>>>>>>>>>>> get_it_demo1_by_id


class Demo222InfoResponse(BaseSchema):
    """获取 it_demo1 by id 响应"""

    id: int = Demo222Fields.id
    name: str = Demo222Fields.name
    created_at: datetime.datetime = Demo222Fields.created_at
    updated_at: datetime.datetime = Demo222Fields.updated_at


class Demo222InfoResponseModel(StandardResponse):
    """获取 it_demo1 by id 响应 Model"""

    data: Demo222InfoResponse | None = None


# ======================>>>>>>>>>>>>>>>>>>>>>> update_it_demo1_by_id


class Demo222UpdateRequest(BaseSchema):
    """更新 it_demo1 by id 请求"""

    name: str = Demo222Fields.name


class Demo222UpdateResponse(BaseSchema):
    """更新 it_demo1 by id 响应"""

    id: int = Demo222Fields.id
    name: str = Demo222Fields.name


class Demo222UpdateResponseModel(StandardResponse):
    """更新 it_demo1 by id 响应 Model"""

    data: Demo222UpdateResponse | None = None


# ======================>>>>>>>>>>>>>>>>>>>>>> delete_it_demo1_by_id


class Demo222DeleteResponse(BaseSchema):
    """删除 it_demo1 by id 响应"""

    id: int = Demo222Fields.id


class Demo222DeleteResponseModel(StandardResponse):
    """删除 it_demo1 by id 响应 Model"""

    data: Demo222DeleteResponse | None = None
