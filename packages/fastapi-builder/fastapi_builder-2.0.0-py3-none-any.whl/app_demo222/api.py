import datetime
from typing import List
from fastapi import APIRouter, Body, Depends, Path
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from apps.app_demo222 import doc
from apps.app_demo222.schema import (
    Demo222CreateRequest,
    Demo222CreateResponse,
    Demo222CreateResponseModel,
    Demo222DeleteResponse,
    Demo222DeleteResponseModel,
    Demo222InfoResponse,
    Demo222InfoResponseModel,
    Demo222ListQueryRequest,
    Demo222ListResponse,
    Demo222ListResponseModel,
    Demo222UpdateRequest,
    Demo222UpdateResponse,
    Demo222UpdateResponseModel,
    Demo222sDeleteResponse,
    Demo222sDeleteResponseModel,
    Demo222sPatchRequest,
    Demo222sPatchResponse,
    Demo222sPatchResponseModel,
)
from apps.app_demo222.model import Demo222
from core.e import ErrorCode, ErrorMessage
from db.database import get_async_db
from schemas.base import OrderType
from schemas.response import PaginationResponse


router = APIRouter()


"""
接口：Demo222 表增删改查

GET    /api/demo222s               ->  get_demo222s    ->  获取所有 demo222
POST   /api/demo222s               ->  add_demo222     ->  创建单个 demo222
PATCH  /api/demo222s               ->  patch_demo222s  ->  批量更新 demo222
DELETE /api/demo222s               ->  delete_demo222s ->  批量注销 demo222
GET    /api/demo222s/{demo222_id}  ->  get_demo222     ->  获取单个 demo222
PUT    /api/demo222s/{demo222_id}  ->  update_demo222  ->  更新单个 demo222
DELETE /api/demo222s/{demo222_id}  ->  delete_demo222  ->  注销单个 demo222
"""


@router.get(
    "",
    name="获取所有 demo222",
    response_model=Demo222ListResponseModel,
    responses=doc.get_demo222s_responses,
)
async def get_demo222s(
    query_params: Demo222ListQueryRequest = Depends(),
    db: AsyncSession = Depends(get_async_db),
):
    # 获取总数
    total_count = (await db.execute(select(func.count()).select_from(Demo222))).scalar()

    # 查询
    stmt = await Demo222.query()
    if query_params.size is not None:
        offset = (query_params.page - 1) * query_params.size
        stmt = stmt.offset(offset).limit(query_params.size)
    if query_params.order_type:
        stmt = stmt.order_by(
            getattr(Demo222, query_params.order_by).desc()
            if query_params.order_type == OrderType.DESC
            else getattr(Demo222, query_params.order_by).asc()
        )

    db_demo222s: List[Demo222] = (await db.execute(stmt)).scalars().all()

    return Demo222ListResponseModel(
        data=PaginationResponse(
            list=[
                Demo222ListResponse.model_validate(
                    db_demo222, from_attributes=True
                ).model_dump()
                for db_demo222 in db_demo222s
            ],
            count=len(db_demo222s),
            page=query_params.page,
            size=query_params.size,
            total=total_count,
        ).model_dump()
    )


@router.post(
    "",
    name="创建单个 demo222",
    response_model=Demo222CreateResponseModel,
    responses=doc.create_demo222_responses,
)
async def create_demo222(
    demo222: Demo222CreateRequest = Body(
        ..., openapi_examples=doc.create_demo222_request
    ),
    db: AsyncSession = Depends(get_async_db),
):
    async with db.begin():
        db_demo222: Demo222 = await Demo222.create(db, **demo222.model_dump())
    return Demo222CreateResponseModel(
        data=Demo222CreateResponse.model_validate(db_demo222, from_attributes=True)
    )


@router.patch(
    "",
    name="批量更新 demo222",
    response_model=Demo222sPatchResponseModel,
    responses=doc.patch_demo222s_responses,
)
async def patch_demo222s(
    demo222s_patch_request: Demo222sPatchRequest = Body(
        ..., openapi_examples=doc.patch_demo222s_request
    ),
    db: AsyncSession = Depends(get_async_db),
):
    async with db.begin():
        stmt = (await Demo222.query()).filter(
            Demo222.id.in_(demo222s_patch_request.ids)
        )
        db_demo222s: List[Demo222] = (await db.execute(stmt)).scalars().all()
        for db_demo222 in db_demo222s:
            db_demo222.name = demo222s_patch_request.name
        db.flush()
    return Demo222sPatchResponseModel(
        data=Demo222sPatchResponse(
            ids=[db_demo222.id for db_demo222 in db_demo222s],
            name=demo222s_patch_request.name,
        )
    )


@router.delete(
    "",
    name="批量注销 demo222",
    response_model=Demo222sDeleteResponseModel,
    responses=doc.delete_demo222s_responses,
)
async def delete_demo222s(
    ids: List[int] = Body(
        ...,
        description="demo222 id 列表",
        embed=True,
        json_schema_extra=doc.delete_demo222s_request,
    ),
    db: AsyncSession = Depends(get_async_db),
):
    async with db.begin():
        stmt_select = (await Demo222.query()).filter(Demo222.id.in_(ids))
        db_demo222s: List[Demo222] = (await db.execute(stmt_select)).scalars().all()

        stmt_update = (
            update(Demo222)
            .where(Demo222.deleted_at.is_(None))
            .filter(Demo222.id.in_(ids))
            .values(deleted_at=datetime.datetime.now())
        )
        await db.execute(stmt_update)
    return Demo222sDeleteResponseModel(
        data=Demo222sDeleteResponse(
            ids=[db_demo222.id for db_demo222 in db_demo222s]
        )
    )


@router.get(
    "/{demo222_id}",
    name="获取单个 demo222 by id",
    response_model=Demo222InfoResponseModel,
    responses=doc.get_demo222_by_id_responses,
)
async def get_demo222_by_id(
    demo222_id: int = Path(..., description="demo222 id", ge=1, example=1),
    db: AsyncSession = Depends(get_async_db),
):
    db_demo222: Demo222 | None = await Demo222.get_by(db, id=demo222_id)
    if db_demo222 is None:
        return Demo222InfoResponseModel(
            code=ErrorCode.NOT_FOUND,
            message=ErrorMessage.get(ErrorCode.NOT_FOUND),
        ).to_json(status_code=HTTP_404_NOT_FOUND)

    return Demo222InfoResponseModel(
        data=Demo222InfoResponse.model_validate(db_demo222, from_attributes=True)
    )


@router.put(
    "/{demo222_id}",
    name="更新单个 demo222 by id",
    response_model=Demo222UpdateResponseModel,
    responses=doc.update_demo222_by_id_responses,
)
async def update_demo222_by_id(
    demo222_id: int = Path(..., description="demo222 id", ge=1),
    demo222_update_request: Demo222UpdateRequest = Body(
        ..., openapi_examples=doc.update_demo222_by_id_request
    ),
    db: AsyncSession = Depends(get_async_db),
):
    async with db.begin():
        db_demo222: Demo222 | None = await Demo222.get_by(db, id=demo222_id)
        if db_demo222 is None:
            return Demo222UpdateResponseModel(
                code=ErrorCode.NOT_FOUND,
                message=ErrorMessage.get(ErrorCode.NOT_FOUND),
            )

        # 更新 name
        if demo222_update_request.name is not None:
            db_demo222.username = demo222_update_request.name

        await db_demo222.save(db)

    return Demo222UpdateResponseModel(
        data=Demo222UpdateResponse.model_validate(
            db_demo222, from_attributes=True
        ).model_dump(),
    )


@router.delete(
    "/{demo222_id}",
    name="注销单个 demo222 by id",
    response_model=Demo222DeleteResponseModel,
    responses=doc.delete_demo222_by_id_responses,
)
async def delete_demo222_by_id(
    demo222_id: int = Path(..., description="demo222 id", ge=1),
    db: AsyncSession = Depends(get_async_db),
):
    async with db.begin():
        db_demo222: Demo222 | None = await Demo222.get_by(db, id=demo222_id)
        if db_demo222 is None:
            return Demo222DeleteResponseModel(
                code=ErrorCode.NOT_FOUND,
                message=ErrorMessage.get(ErrorCode.NOT_FOUND),
            ).to_json(status_code=HTTP_404_NOT_FOUND)
        await db_demo222.remove(db)

    return Demo222DeleteResponseModel(data=Demo222DeleteResponse(id=db_demo222.id))
