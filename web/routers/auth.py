from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from typing import Optional
from tjw.core.db import get_db, log_operation

router = APIRouter()


class LoginResponse(BaseModel):
    success: bool = Field(description="登录是否成功")
    message: str = Field(description="提示信息")
    data: Optional[dict] = Field(None, description="用户信息")


class ChangePasswordResponse(BaseModel):
    success: bool = Field(description="修改是否成功")
    message: str = Field(description="提示信息")


class ResetPasswordResponse(BaseModel):
    success: bool = Field(description="重置是否成功")
    message: str = Field(description="提示信息")


@router.post("/login", response_model=LoginResponse, summary="用户登录")
async def login(
    username: str = Query(..., description="用户名"),
    password: str = Query(..., description="密码")
):
    """
    用户登录接口
    
    默认用户名/密码: admin/admin
    
    - **username**: 用户名
    - **password**: 密码
    """
    db = get_db()
    user = db.verify_user(username, password)
    
    if user:
        log_operation('login', 'auth', f'用户 {username} 登录成功')
        return {
            "success": True,
            "message": "登录成功",
            "data": user.to_dict()
        }
    
    log_operation('login_failed', 'auth', f'用户 {username} 登录失败')
    return {
        "success": False,
        "message": "用户名或密码错误",
        "data": None
    }


@router.post("/change-password", response_model=ChangePasswordResponse, summary="修改密码")
async def change_password(
    username: str = Query(..., description="用户名"),
    old_password: str = Query(..., description="旧密码"),
    new_password: str = Query(..., description="新密码")
):
    """
    修改用户密码
    
    - **username**: 用户名
    - **old_password**: 旧密码
    - **new_password**: 新密码
    """
    db = get_db()
    
    user = db.verify_user(username, old_password)
    if not user:
        return {
            "success": False,
            "message": "旧密码错误"
        }
    
    if len(new_password) < 1:
        return {
            "success": False,
            "message": "新密码长度至少1位"
        }
    
    result = db.update_user_password(username, new_password)
    
    if result:
        log_operation('change_password', 'auth', f'用户 {username} 修改密码成功')
        return {
            "success": True,
            "message": "密码修改成功"
        }
    
    return {
        "success": False,
        "message": "密码修改失败"
    }


@router.post("/reset-password", response_model=ResetPasswordResponse, summary="重置密码（忘记密码）")
async def reset_password():
    """
    重置管理员密码为默认值
    
    通过执行SQL脚本将管理员密码恢复为默认值 admin/admin
    
    **操作说明**:
    1. 关闭应用程序
    2. 删除 data/tjw.db 文件，重新启动应用会自动初始化管理员账户
    3. 或者执行以下SQL语句：
       UPDATE users SET password_hash = '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918' WHERE username = 'admin';
    """
    db = get_db()
    result = db.reset_admin_password()
    
    if result:
        log_operation('reset_password', 'auth', '管理员密码已重置为默认值')
        return {
            "success": True,
            "message": "管理员密码已重置为默认值 admin/admin"
        }
    
    return {
        "success": False,
        "message": "密码重置失败"
    }


@router.get("/reset-guide", summary="忘记密码操作指南")
async def get_reset_guide():
    """
    获取忘记密码的操作指南
    """
    return {
        "success": True,
        "message": "忘记密码操作指南",
        "data": {
            "method": "SQL脚本恢复",
            "steps": [
                "方法一：删除数据库文件",
                "1. 关闭应用程序",
                "2. 删除 data/tjw.db 文件",
                "3. 重新启动应用，系统会自动创建管理员账户（admin/admin）",
                "",
                "方法二：执行SQL语句（需要SQLite客户端）",
                "1. 使用SQLite客户端连接 data/tjw.db",
                "2. 执行SQL: UPDATE users SET password_hash = '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918' WHERE username = 'admin';",
                "3. 重新启动应用即可使用 admin/admin 登录"
            ],
            "default_credentials": {
                "username": "admin",
                "password": "admin"
            }
        }
    }