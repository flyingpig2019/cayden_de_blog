# -*- coding: utf-8 -*-
"""
工具函数模块
包含各种辅助功能的实用函数
"""

import re
import urllib.parse

def convert_youtube_url(url):
    """
    将YouTube URL转换为嵌入格式
    支持多种YouTube URL格式，包括短链接(youtu.be)
    
    参数:
        url: YouTube视频URL
        
    返回:
        转换后的嵌入URL
    """
    if not url:
        return None
        
    # 处理youtu.be短链接
    youtu_be_pattern = r'youtu\.be\/([\w-]+)'
    youtu_be_match = re.search(youtu_be_pattern, url)
    if youtu_be_match:
        video_id = youtu_be_match.group(1)
        return f'https://www.youtube.com/embed/{video_id}'
    
    # 处理标准YouTube链接
    youtube_pattern = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/ ]{11})'
    youtube_match = re.search(youtube_pattern, url)
    if youtube_match:
        video_id = youtube_match.group(1)
        return f'https://www.youtube.com/embed/{video_id}'
    
    # 如果已经是嵌入格式，直接返回
    if 'youtube.com/embed/' in url:
        return url
        
    # 无法识别的格式，返回原始URL
    return url

def log_debug(message):
    import os
    import datetime
    log_file_path = os.path.join(os.getcwd(), 'debug_log.txt')
    with open(log_file_path, 'a') as f:
        f.write(f"[DEBUG] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")