from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, Dict
import os
import re
import sys
import subprocess
import requests
from tjw import __version__

router = APIRouter()

LOCAL_VERSION = __version__
PACKAGE_NAME = "tjw"


class VersionInfo(BaseModel):
    success: bool = Field(description="请求是否成功")
    message: str = Field(description="提示信息")
    data: Optional[Dict] = Field(None, description="版本信息数据")


class UpgradeResponse(BaseModel):
    success: bool = Field(description="升级是否成功")
    message: str = Field(description="升级结果消息")
    progress: int = Field(description="升级进度(0-100)")
    current_step: str = Field(description="当前步骤")


def get_pypi_version() -> str:
    """获取PyPI上的最新版本"""
    try:
        url = f"https://pypi.org/pypi/{PACKAGE_NAME}/json"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            releases = list(data["releases"].keys())
            releases.sort(key=lambda x: tuple(map(int, x.split("."))))
            return releases[-1] if releases else LOCAL_VERSION
    except Exception as e:
        print(f"获取PyPI版本失败: {e}")
    return LOCAL_VERSION


def compare_versions(v1: str, v2: str) -> int:
    """比较两个版本号，返回-1, 0, 1"""
    parts1 = list(map(int, v1.split(".")))
    parts2 = list(map(int, v2.split(".")))
    for p1, p2 in zip(parts1, parts2):
        if p1 < p2:
            return -1
        if p1 > p2:
            return 1
    return len(parts1) - len(parts2)


@router.get("/version", response_model=VersionInfo, summary="获取版本信息")
async def get_version_info():
    """
    获取当前版本和PyPI最新版本信息
    """
    pypi_version = get_pypi_version()
    has_update = compare_versions(LOCAL_VERSION, pypi_version) < 0
    
    return {
        "success": True,
        "message": "获取成功",
        "data": {
            "current_version": LOCAL_VERSION,
            "pypi_version": pypi_version,
            "has_update": has_update,
            "update_available": has_update,
            "package_name": PACKAGE_NAME
        }
    }


@router.post("/upgrade", summary="执行升级")
async def perform_upgrade():
    """
    执行升级操作，返回升级进度
    """
    import asyncio
    
    result = {
        "success": False,
        "message": "",
        "progress": 0,
        "current_step": "开始升级..."
    }
    
    try:
        # 步骤1: 检查新版本
        result["current_step"] = "正在检查新版本..."
        result["progress"] = 10
        pypi_version = get_pypi_version()
        
        if not compare_versions(LOCAL_VERSION, pypi_version) < 0:
            result["message"] = "当前已是最新版本"
            result["progress"] = 100
            return result
        
        # 步骤2: 执行pip升级（使用--no-deps避免依赖问题）
        result["current_step"] = f"正在下载并安装新版本 {pypi_version}..."
        result["progress"] = 30
        
        upgrade_cmd = [sys.executable, "-m", "pip", "install", "--upgrade", PACKAGE_NAME, "--no-deps"]
        process = subprocess.run(upgrade_cmd, capture_output=True, text=True, encoding='utf-8')
        
        if process.returncode != 0:
            raise Exception(f"升级失败: {process.stderr[:200]}")
        
        result["progress"] = 80
        result["current_step"] = "升级完成，请手动重启服务..."
        
        result["success"] = True
        result["message"] = f"升级成功！已从 v{LOCAL_VERSION} 升级到 v{pypi_version}\n请手动重启服务以应用更新"
        result["progress"] = 100
        result["current_step"] = "升级完成"
        
    except Exception as e:
        result["message"] = f"升级失败: {str(e)[:200]}"
        result["current_step"] = "升级失败"
    
    return result