#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TJW API 启动脚本
"""
import subprocess
import sys
import os

def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        🚀 TJW FastAPI Service                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐  ║
║  │  🏠 首页          │  http://localhost:8000/                           │  ║
║  │  📖 API文档       │  http://localhost:8000/docs                      │  ║
║  │  📘 Redoc文档     │  http://localhost:8000/redoc                     │  ║
║  │  🏥 健康检查      │  http://localhost:8000/health                    │  ║
║  │  🔌 API基础路径    │  http://localhost:8000/api/sfz                  │  ║
║  └────────────────────────────────────────────────────────────────────────┘  ║
║                                                                              ║
║  ┌──────────────────────── 快捷访问 ─────────────────────────┐              ║
║  │  🆔 身份证工具    │  /id/1002 或 /?id=1002  例：http://localhost:8000/id/1002  │              ║
║  │  📊 仪表盘        │  /id/1001 或 /?id=1001              │              ║
║  │  🔧 实用工具      │  /id/1003 或 /?id=1003              │              ║
║  │  ⚙️ 系统设置      │  /id/1004 或 /?id=1004              │              ║
║  └────────────────────────────────────────────────────────────────────────┘  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def main():
    print("\n" + "="*70)
    print("          📦 正在启动 TJW FastAPI 服务...")
    print("="*70)
    
    # 确保依赖已安装
    try:
        import fastapi
        import uvicorn
        import pydantic
        print("✅ 依赖检查通过")
    except ImportError:
        print("⚠️  检测到依赖未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "pydantic"], check=True)
        print("✅ 依赖安装完成")
    
    print("\n🚀 启动服务...")
    
    # 启动 uvicorn
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "web.app:app", 
        "--host", "0.0.0.0", 
        "--port", "8000", 
        "--reload"
    ]
    
    try:
        # 先打印启动成功后的信息
        print("\n" + "="*70)
        print_banner()
        print("💡 提示: 按 Ctrl+C 停止服务")
        print("="*70 + "\n")
        
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n✅ 服务已停止")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 服务启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()