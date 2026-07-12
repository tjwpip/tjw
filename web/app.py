from fastapi import FastAPI, Path, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from web.routers import sfz_router
from tjw.core.shengfenzheng.sfz import CShengFenZheng

# 创建 FastAPI 应用
app = FastAPI(
    title="TJW API",
    description="TJW 私人项目 API 接口文档",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 模块ID映射
MODULE_MAP = {
    1001: "dashboard",    # 仪表盘
    1002: "sfz",          # 身份证工具
    1003: "tools",        # 实用工具
    1004: "settings"      # 系统设置
}

# 初始化身份证工具
sfz_tool = CShengFenZheng()

# 注册路由
app.include_router(sfz_router, prefix="/api/sfz", tags=["身份证工具"])

# 挂载静态文件
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# 根路径 - 显示首页（支持模块ID参数）
@app.get("/", tags=["首页"])
async def root(id: int = Query(None, description="模块ID")):
    return FileResponse("web/static/index.html")

# 简洁路径访问 /id/{id}
@app.get("/id/{id}", tags=["快捷访问"])
async def quick_access(id: int = Path(description="模块ID")):
    if id in MODULE_MAP:
        return RedirectResponse(url=f"/?id={id}")
    return RedirectResponse(url="/")

# 健康检查接口
@app.get("/health", tags=["健康检查"])
async def health_check():
    return {"status": "healthy", "service": "TJW API"}

# 模块列表接口
@app.get("/api/modules", tags=["模块管理"])
async def get_modules():
    return {
        "success": True,
        "data": [
            {"id": 1001, "name": "仪表盘", "key": "dashboard", "icon": "📊"},
            {"id": 1002, "name": "身份证工具", "key": "sfz", "icon": "🆔"},
            {"id": 1003, "name": "实用工具", "key": "tools", "icon": "🔧"},
            {"id": 1004, "name": "系统设置", "key": "settings", "icon": "⚙️"}
        ]
    }

# 启动命令：uvicorn web.app:app --host 0.0.0.0 --port 8000 --reload