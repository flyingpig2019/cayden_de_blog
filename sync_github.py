import os
import time
import git
from git import Repo
from git.exc import GitCommandError
from flask import Flask, jsonify, request

def update_to_github(username, password, repo_url):
    """
    将本地文件单向更新到GitHub仓库（不会拉取远程更改）
    
    Args:
        username: GitHub用户名
        password: GitHub密码
        repo_url: GitHub仓库URL
    
    Returns:
        dict: 包含更新结果的字典
    """
    try:
        # 获取当前工作目录
        current_dir = os.getcwd()
        
        # 构建带有凭据的远程URL
        remote_url = repo_url.replace('https://', f'https://{username}:{password}@')
        
        # 检查是否已经初始化了Git仓库
        if not os.path.exists(os.path.join(current_dir, '.git')):
            # 初始化Git仓库
            repo = Repo.init(current_dir)
            
            # 配置远程仓库URL
            origin = repo.create_remote('origin', remote_url)
        else:
            # 打开现有仓库
            repo = Repo(current_dir)
            
            # 检查是否已有origin远程
            try:
                origin = repo.remote('origin')
                # 更新远程URL
                repo.git.remote('set-url', 'origin', remote_url)
            except ValueError:
                # 如果没有origin远程，创建一个
                origin = repo.create_remote('origin', remote_url)
        
        # 配置Git用户信息（如果尚未配置）
        if not repo.config_reader().has_section('user'):
            repo.config_writer().set_value("user", "name", "Cayden Blog Sync").release()
            repo.config_writer().set_value("user", "email", "cayden.sync@example.com").release()
        
        # 添加所有文件到暂存区
        repo.git.add(A=True)
        
        # 检查是否有要提交的更改
        if repo.is_dirty() or len(repo.untracked_files) > 0:
            # 提交更改
            commit_message = f'Auto sync at {time.strftime("%Y-%m-%d %H:%M:%S")}'
            repo.git.commit('-m', commit_message)
            
            # 确定当前分支名称
            try:
                branch_name = repo.active_branch.name
            except TypeError:
                # 如果没有活动分支，默认使用main
                branch_name = 'main'

            # 检查并创建或切换到main分支
            if branch_name != 'main':
                try:
                    repo.git.checkout('main')
                    branch_name = 'main'
                except GitCommandError:
                    # 如果main分支不存在，则创建它
                    repo.git.checkout('-b', 'main')
                    branch_name = 'main'
            
            # 跳过拉取远程更改（单向更新）
            print("跳过拉取远程更改（单向更新模式）")

            # 推送到GitHub
            push_info = origin.push(branch_name)
            
            # 检查推送结果
            for info in push_info:
                if info.flags & info.ERROR:
                    return {
                        'success': False,
                        'message': f'推送失败: {info.summary}',
                        'error': info.summary,
                        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                    }
            
            return {
                'success': True,
                'message': '成功同步到GitHub仓库',
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            return {
                'success': True,
                'message': '没有更改需要同步',
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
            }
    except GitCommandError as e:
        # 处理Git命令错误
        error_msg = str(e)
        
        # 如果是分支问题，尝试使用不同的分支名
        if ('main' in error_msg or 'master' in error_msg) and 'push' in error_msg:
            try:
                repo = Repo(os.getcwd())
                # 尝试使用另一个分支名
                alt_branch = 'master' if 'main' in error_msg else 'main'
                push_info = repo.remote('origin').push(alt_branch)
                
                return {
                    'success': True,
                    'message': f'成功同步到GitHub仓库（使用{alt_branch}分支）',
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                }
            except GitCommandError as e2:
                return {
                    'success': False,
                    'message': f'同步失败: {str(e2)}',
                    'error': str(e2),
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                }
        
        return {
            'success': False,
            'message': f'同步失败: {error_msg}',
            'error': error_msg,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'同步失败: {str(e)}',
            'error': str(e),
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        }