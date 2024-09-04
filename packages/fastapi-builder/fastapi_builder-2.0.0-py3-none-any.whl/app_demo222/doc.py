from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
)

from core.e import ErrorCode, ErrorMessage
from schemas.response import StandardResponse

# common

NOT_FOUND = {
    "description": "demo222 不存在.",
    "model": StandardResponse,
    "content": {
        "application/json": {
            "example": {
                "code": ErrorCode.NOT_FOUND,
                "message": ErrorMessage.get(ErrorCode.NOT_FOUND),
            }
        }
    },
}

# ======================>>>>>>>>>>>>>>>>>>>>>> get_demo222

get_demo222s_responses = {
    HTTP_200_OK: {
        "description": "获取 demo222 列表成功",
        "content": {
            "application/json": {
                "example": {
                    "code": 0,
                    "data": {
                        "list": [
                            {
                                "id": 1,
                                "name": "test1",
                            },
                            {
                                "id": 2,
                                "name": "test02",
                            }
                        ],
                        "count": 2,
                        "total": 5,
                        "page": 1,
                        "size": 2
                    },
                    "message": "",
                }
            }
        },
    }
}

# ======================>>>>>>>>>>>>>>>>>>>>>> create_demo222

create_demo222_request = {
    "创建 demo222": {
        "description": "创建时需要输入 <u>**name**</u>.",
        "value": {
            "name": "new_name",
        }
    }
}

create_demo222_responses = {
    HTTP_200_OK: {
        "description": "创建 demo222 成功",
        "content": {
            "application/json": {
                "example": {
                    "code": 0,
                    "data": {
                        "id": 1,
                        "name": "new_name",
                    },
                    "message": "",
                }
            }
        }
    }
}

# ======================>>>>>>>>>>>>>>>>>>>>>> patch_demo222s

patch_demo222s_responses = {
    HTTP_200_OK: {
        "description": "批量更新 demo222 成功",
        "content": {
            "application/json": {
                "example": {
                    "code": 0,
                    "data": {
                        "ids": [1, 2],
                        "name": "new_name",
                    },
                    "message": "",
                }
            }
        }
    }
}

patch_demo222s_request = {
    "批量更新 demo222 name": {
        "description": "批量更新 demo222，返回更新成功的 demo222 id 和更新条目",
        "value": {
            "ids": [1, 2, 3],
            "name": "new_name",
        },
    }
}

# ======================>>>>>>>>>>>>>>>>>>>>>> delete_demo222s

delete_demo222s_responses = {
    HTTP_200_OK: {
        "description": "批量删除 demo222 成功",
        "content": {
            "application/json": {
                "example": {
                    "code": 0,
                    "data": {
                        "ids": [1, 2],
                    },
                    "message": "",
                }
            }
        }
    }
}

delete_demo222s_request = {
    "example": [1, 2, 3],
}

# ======================>>>>>>>>>>>>>>>>>>>>>> get_demo222_by_id

get_demo222_by_id_responses = {
    HTTP_200_OK: {
        "description": "获取 demo222 信息成功.",
        "content": {
            "application/json": {
                "example": {
                    "code": 0,
                    "message": "",
                    "data": {
                        "id": 1,
                        "name": "demo222",
                        "created_at": "2023-07-03 08:03:03",
                        "updated_at": "2023-07-03 08:03:03",
                    },
                }
            }
        },
    },
    HTTP_404_NOT_FOUND: NOT_FOUND,
}

# ======================>>>>>>>>>>>>>>>>>>>>>> update_demo222_by_id

update_demo222_by_id_responses = {
    HTTP_200_OK: {
        "description": "更改 demo222 成功",
        "content": {
            "application/json": {
                "example": {
                    "code": 0,
                    "data": {
                        "id": 1,
                        "name": "new_name",
                    },
                    "message": "",
                },
            },
        },
    },
    HTTP_404_NOT_FOUND: NOT_FOUND,
}

update_demo222_by_id_request = {
    "更新 name": {
        "description": "设置 `name` 为新值.",
        "value": {
            "name": "new_name",
        },
    },
}

# ======================>>>>>>>>>>>>>>>>>>>>>> delete_demo222_by_id

delete_demo222_by_id_responses = {
    HTTP_200_OK: {
        "description": "注销 demo222 成功",
        "content": {
            "application/json": {
                "example": {
                    "code": 0,
                    "data": {
                        "id": 1,
                    },
                    "message": ""
                },
            },
        },
    },
    HTTP_404_NOT_FOUND: NOT_FOUND,
}
