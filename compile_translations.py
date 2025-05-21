#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
编译翻译文件的脚本
运行此脚本将编译所有翻译文件，使其在应用程序中可用
"""

import os
import subprocess
import sys

def main():
    print("开始编译翻译文件...")
    try:
        # 检查translations目录是否存在
        if not os.path.exists('translations'):
            print("错误：translations目录不存在。请先运行以下命令提取和初始化翻译：")
            print("pybabel extract -F babel.cfg -o messages.pot .")
            print("pybabel init -i messages.pot -d translations -l zh")
            return 1
        
        # 编译翻译
        result = subprocess.run(['pybabel', 'compile', '-d', 'translations'], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            print("翻译文件编译成功！")
            print("现在您可以通过在应用程序中切换语言来查看翻译。")
            return 0
        else:
            print("编译翻译文件时出错：")
            print(result.stderr)
            return 1
    
    except Exception as e:
        print(f"发生错误：{e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())