from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, Dict
import os
import platform
from tjw import __version__

router = APIRouter()


class AboutResponse(BaseModel):
    success: bool = Field(description="请求是否成功")
    message: str = Field(description="提示信息")
    data: Optional[Dict] = Field(None, description="关于信息")


@router.get("/about", response_model=AboutResponse, summary="获取关于信息")
async def get_about():
    """
    获取系统版本号及相关信息
    """
    about_info = {
        "version": __version__,
        "name": "TJW 工具平台",
        "description": "提供身份证工具等实用功能的个人工作站和API服务",
        "author": "TJW Developer",
        "email": "developer@tjw.local",
        "copyright": "2026 TJW. All rights reserved.",
        "system": {
            "python_version": platform.python_version(),
            "platform": platform.system(),
            "release": platform.release(),
            "machine": platform.machine()
        },
        "features": [
            "身份证号码生成",
            "身份证号码验证",
            "身份证地区查询",
            "批量身份证生成",
            "用户登录与认证",
            "密码修改功能",
            "操作日志记录"
        ],
        "api_endpoints": {
            "Swagger文档": "/docs",
            "Redoc文档": "/redoc",
            "健康检查": "/health",
            "模块列表": "/api/modules",
            "认证接口": "/api/auth/",
            "身份证接口": "/api/sfz/",
            "关于接口": "/api/about/"
        }
    }

    return {
        "success": True,
        "message": "获取成功",
        "data": about_info
    }


@router.get("/version", summary="获取版本号")
async def get_version():
    """
    获取当前系统版本号
    """
    return {
        "success": True,
        "version": "1.0.0",
        "build": "20240101"
    }
