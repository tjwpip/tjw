#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TJW API 启动脚本
"""
import subprocess
import sys
import os
import socket

def find_available_port(start_port=8000, max_port=8100):
    """查找可用端口"""
    for port in range(start_port, max_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("0.0.0.0", port))
                return port
            except socket.error:
                continue
    return None

def print_banner(port):
    banner = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        🚀 TJW FastAPI Service                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐  ║
║  │  🏠 首页          │  http://localhost:{port}/                           │  ║
║  │  📖 API文档       │  http://localhost:{port}/docs                      │  ║
║  │  📘 Redoc文档     │  http://localhost:{port}/redoc                     │  ║
║  │  🏥 健康检查      │  http://localhost:{port}/health                    │  ║
║  │  🔌 API基础路径    │  http://localhost:{port}/api/sfz                  │  ║
║  └────────────────────────────────────────────────────────────────────────┘  ║
║                                                                              ║
║  ┌──────────────────────── 快捷访问 ─────────────────────────┐              ║
║  │  🆔 身份证工具    │  /id/1002 或 /?id=1002  例：http://localhost:{port}/id/1002  │              ║
║  │  📊 仪表盘        │  /id/1001 或 /?id=1001              │              ║
║  │  🔧 实用工具      │  /id/1003 或 /?id=1003              │              ║
║  │  ⚙️ 系统设置      │  /id/1004 或 /?id=1004              │              ║
║  │  ⬆️ 升级更新      │  /id/1007 或 /?id=1007              │              ║
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
        print("⚠️ 检测到依赖未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "pydantic"], check=True)
        print("✅ 依赖安装完成")
    
    # 查找可用端口
    print("\n🔍 正在检测可用端口...")
    port = find_available_port(8000, 8100)
    
    if port is None:
        print("❌ 未找到可用端口 (8000-8100)")
        sys.exit(1)
    
    if port != 8000:
        print(f"ℹ️  默认端口 8000 被占用，自动切换到端口 {port}")
    else:
        print(f"✅ 端口 {port} 可用")
    
    print("\n🚀 启动服务...")
    
    # 启动 uvicorn
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "web.app:app", 
        "--host", "0.0.0.0", 
        "--port", str(port), 
        "--reload"
    ]
    
    try:
        # 先打印启动成功后的信息
        print("\n" + "="*70)
        print_banner(port)
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
