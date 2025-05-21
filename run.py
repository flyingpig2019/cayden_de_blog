#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
启动凯登的成长博客应用程序
此脚本将检查必要的目录是否存在，检查依赖项是否安装，并启动Flask应用程序
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

def check_dependencies():
    """检查requirements.txt中列出的所有依赖项是否已安装，并验证版本兼容性"""
    print("正在检查依赖项...")
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("警告: requirements.txt文件不存在，无法检查依赖项。")
        return False
    
    # 读取requirements.txt文件
    with open(requirements_file, "r") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    
    # 特殊包名到模块名的映射
    package_to_module = {
        "Flask-Babel": "flask_babel",
        "python-dotenv": "dotenv"
    }
    
    missing_packages = []
    incompatible_packages = []
    
    # 检查Flask-Babel版本兼容性问题
    flask_babel_version = None
    for req in requirements:
        if req.startswith("Flask-Babel"):
            parts = req.split("==")
            if len(parts) > 1:
                flask_babel_version = parts[1]
    
    # 如果Flask-Babel版本是3.x，需要降级到2.x版本
    if flask_babel_version and flask_babel_version.startswith("3"):
        print(f"检测到Flask-Babel版本 {flask_babel_version} 可能与应用程序不兼容")
        print("Flask-Babel 3.x版本移除了localeselector装饰器，需要使用2.x版本")
        incompatible_packages.append("Flask-Babel==2.0.0")
    
    for package in requirements:
        package_name = package.split("==")[0]
        # 跳过已知不兼容的包
        if any(package_name in p for p in incompatible_packages):
            continue
            
        # 检查包是否已安装
        module_name = package_to_module.get(package_name, package_name.replace("-", "_").lower())
        try:
            # 尝试导入模块
            importlib.import_module(module_name)
        except ImportError:
            missing_packages.append(package)
    
    need_install = False
    
    if missing_packages:
        print(f"发现缺少的依赖项: {', '.join(missing_packages)}")
        need_install = True
    
    if incompatible_packages:
        print(f"发现不兼容的依赖项，需要安装特定版本: {', '.join(incompatible_packages)}")
        need_install = True
    
    if need_install:
        install = input("是否要安装/更新这些依赖项? (y/n): ").lower().strip()
        if install == 'y':
            print("正在安装/更新依赖项...")
            try:
                # 如果有不兼容的包，先卸载它们
                if incompatible_packages:
                    for package in incompatible_packages:
                        package_name = package.split('==')[0]
                        print(f"卸载 {package_name}...")
                        subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", package_name], check=True)
                
                # 安装缺失的包
                if missing_packages:
                    print("安装缺失的依赖项...")
                    for package in missing_packages:
                        print(f"安装 {package}...")
                        subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
                
                # 安装特定版本的不兼容包
                if incompatible_packages:
                    print("安装特定版本的依赖项...")
                    for package in incompatible_packages:
                        print(f"安装 {package}...")
                        subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
                
                print("依赖项安装/更新成功！")
                return True
            except subprocess.CalledProcessError as e:
                print(f"错误: 依赖项安装/更新失败。{str(e)}")
                return False
        else:
            print("警告: 缺少必要的依赖项或存在不兼容的依赖项，应用程序可能无法正常运行。")
            return False
    
    print("所有依赖项已安装且兼容。")
    return True

def main():
    print("正在启动凯登的成长博客应用程序...")
    
    # 首先检查依赖项
    if not check_dependencies():
        print("错误: 缺少必要的依赖项，无法继续运行应用程序。")
        return 1
    
    # 检查上传目录是否存在
    uploads_dir = Path("static/uploads")
    if not uploads_dir.exists():
        print(f"创建上传目录: {uploads_dir}")
        uploads_dir.mkdir(parents=True, exist_ok=True)
    
    # 检查translations目录是否存在
    translations_dir = Path("translations")
    if not translations_dir.exists():
        print("警告: translations目录不存在。多语言支持可能不可用。")
        print("提示: 运行 init_translations.py 脚本来初始化翻译文件。")
    
    # 检查数据库文件是否存在
    db_file = Path("database.db")
    if not db_file.exists():
        print("数据库文件不存在，正在初始化数据库...")
        try:
            subprocess.run([sys.executable, "-m", "flask", "init-db"], check=True)
            print("数据库初始化成功！")
        except subprocess.CalledProcessError:
            print("错误: 数据库初始化失败。")
            return 1
    
    # 检查.env文件是否存在
    env_file = Path(".env")
    if not env_file.exists():
        env_example = Path(".env.example")
        if env_example.exists():
            print("警告: .env文件不存在，但找到了.env.example文件。")
            print("请复制.env.example到.env并填写您的配置。")
        else:
            print("警告: 未找到.env文件。应用程序可能无法正常工作。")
    
    # 启动Flask应用程序
    print("正在启动Flask应用程序...")
    print("您可以在浏览器中访问: http://127.0.0.1:5000")
    os.environ["FLASK_APP"] = "app.py"
    os.environ["PYTHONUNBUFFERED"] = "1"  # 确保Python输出不被缓冲
    
    # 使用Popen而不是run，这样可以更好地处理信号
    try:
        # 直接启动Flask应用，并将输出重定向到标准输出和标准错误
        process = subprocess.Popen(
            [sys.executable, "-m", "flask", "run"],
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        
        # 等待进程完成或被中断
        process.wait()
        return process.returncode
    except KeyboardInterrupt:
        print("\n应用程序已被用户中断，正在关闭...")
        # 尝试优雅地终止进程
        if 'process' in locals() and process.poll() is None:
            process.terminate()
            try:
                # 给进程一些时间来清理
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # 如果进程没有及时终止，强制终止它
                process.kill()
        return 0
    except Exception as e:
        print(f"\n应用程序运行出错: {str(e)}")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n应用程序已被用户中断，正在关闭...")
        sys.exit(0)