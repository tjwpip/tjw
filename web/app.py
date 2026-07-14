import os
from fastapi import FastAPI, Path, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from web.routers import sfz_router, auth_router, about_router
from tjw.core.shengfenzheng.sfz import CShengFenZheng

app = FastAPI(
    title="TJW API",
    description="TJW 绉佷汉椤圭洰 API 鎺ュ彛鏂囨。",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

MODULE_MAP = {
    1001: "dashboard",
    1002: "sfz",
    1003: "tools",
    1004: "settings",
    1005: "auth",
    1006: "about"
}

sfz_tool = CShengFenZheng()

app.include_router(sfz_router, prefix="/api/sfz", tags=["身份证工具"])
app.include_router(auth_router, prefix="/api/auth", tags=["用户认证"])
app.include_router(about_router, prefix="/api/about", tags=["关于"])

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")


@app.get("/", tags=["首页"])
async def root(id: int = Query(None, description="模块ID")):
    return FileResponse(os.path.join(os.path.dirname(__file__), "static/index.html"))


@app.get("/id/{id}", tags=["快捷访问"])
async def quick_access(id: int = Path(description="模块ID")):
    if id in MODULE_MAP:
        return RedirectResponse(url=f"/?id={id}")
    return RedirectResponse(url="/")


@app.get("/health", tags=["健康检查"])
async def health_check():
    return {"status": "healthy", "service": "TJW API"}


@app.get("/api/modules", tags=["模块管理"])
async def get_modules():
    return {
        "success": True,
        "data": [
            {"id": 1001, "name": "仪表盘", "key": "dashboard", "icon": "📊"},
            {"id": 1002, "name": "身份证工具", "key": "sfz", "icon": "🆔"},
            {"id": 1003, "name": "实用工具", "key": "tools", "icon": "🛠️"},
            {"id": 1004, "name": "系统设置", "key": "settings", "icon": "⚙️"},
            {"id": 1005, "name": "用户管理", "key": "auth", "icon": "👤"},
            {"id": 1006, "name": "关于", "key": "about", "icon": "ℹ️"}
        ]
    }