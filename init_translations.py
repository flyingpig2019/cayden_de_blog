#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
初始化翻译文件的脚本
运行此脚本将提取所有需要翻译的字符串并初始化中文翻译文件
"""

import os
import subprocess
import sys

def main():
    print("开始初始化翻译文件...")
    try:
        # 检查babel.cfg文件是否存在
        if not os.path.exists('babel.cfg'):
            print("错误：babel.cfg文件不存在。请确保该文件存在于项目根目录中。")
            return 1
        
        # 提取需要翻译的字符串
        print("正在提取需要翻译的字符串...")
        extract_result = subprocess.run(['pybabel', 'extract', '-F', 'babel.cfg', '-o', 'messages.pot', '.'], 
                                      capture_output=True, text=True)
        
        if extract_result.returncode != 0:
            print("提取翻译字符串时出错：")
            print(extract_result.stderr)
            return 1
        
        # 检查translations目录是否存在，如果不存在则创建
        if not os.path.exists('translations'):
            os.makedirs('translations')
        
        # 检查中文翻译文件是否已存在
        zh_po_path = os.path.join('translations', 'zh', 'LC_MESSAGES', 'messages.po')
        if os.path.exists(zh_po_path):
            # 更新现有的翻译文件
            print("正在更新现有的中文翻译文件...")
            update_result = subprocess.run(['pybabel', 'update', '-i', 'messages.pot', '-d', 'translations', '-l', 'zh'], 
                                         capture_output=True, text=True)
            if update_result.returncode != 0:
                print("更新翻译文件时出错：")
                print(update_result.stderr)
                return 1
        else:
            # 初始化新的翻译文件
            print("正在初始化新的中文翻译文件...")
            init_result = subprocess.run(['pybabel', 'init', '-i', 'messages.pot', '-d', 'translations', '-l', 'zh'], 
                                       capture_output=True, text=True)
            if init_result.returncode != 0:
                print("初始化翻译文件时出错：")
                print(init_result.stderr)
                return 1
        
        print("翻译文件初始化成功！")
        print("现在您可以编辑 translations/zh/LC_MESSAGES/messages.po 文件来添加中文翻译。")
        print("编辑完成后，运行 compile_translations.py 脚本来编译翻译文件。")
        return 0
    
    except Exception as e:
        print(f"发生错误：{e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())