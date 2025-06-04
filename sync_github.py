import os
import time
import subprocess

from utils import log_debug

class GitHubSyncer:
    def sync_repo(self, username, password, repo_url):
        log_debug("[DEBUG] /api/sync_github endpoint hit!")

        try:
            current_dir = os.getcwd()
            log_debug(f"[DEBUG] Current working directory: {current_dir}")

            # 检查是否已经初始化了Git仓库
            if not os.path.exists(os.path.join(current_dir, '.git')):
                # 初始化Git仓库
                subprocess.run(['git', 'init'], cwd=current_dir, check=True)

                # 配置远程仓库URL
                subprocess.run(['git', 'remote', 'add', 'origin', repo_url], cwd=current_dir, check=True)
            else:
                # 检查是否已有origin远程
                try:
                    subprocess.run(['git', 'remote', 'set-url', 'origin', repo_url], cwd=current_dir, check=True)
                except subprocess.CalledProcessError:
                    # 如果没有origin远程，创建一个
                    subprocess.run(['git', 'remote', 'add', 'origin', repo_url], cwd=current_dir, check=True)

            # 配置Git用户信息（如果尚未配置）
            try:
                subprocess.run(['git', 'config', 'user.name'], cwd=current_dir, check=True, capture_output=True)
            except subprocess.CalledProcessError:
                subprocess.run(['git', 'config', 'user.name', 'Cayden Blog Sync'], cwd=current_dir, check=True)
            try:
                subprocess.run(['git', 'config', 'user.email'], cwd=current_dir, check=True, capture_output=True)
            except subprocess.CalledProcessError:
                subprocess.run(['git', 'config', 'user.email', 'cayden.sync@example.com'], cwd=current_dir, check=True)

            # 添加所有文件到暂存区
            subprocess.run(['git', 'add', '.'], cwd=current_dir, check=True)

            # 检查是否有要提交的更改
            status_output = subprocess.run(['git', 'status', '--porcelain'], cwd=current_dir, capture_output=True, text=True, check=True).stdout.strip()
            is_dirty = bool(status_output)
            log_debug(f"[DEBUG] Repo dirty: {is_dirty}")

            if is_dirty:
                # 提交更改
                commit_message = f'Auto sync at {time.strftime("%Y-%m-%d %H:%M:%S")}'
                log_debug(f"[DEBUG] Committing with message: {commit_message}")
                subprocess.run(['git', 'commit', '-m', commit_message], cwd=current_dir, check=True)

                # 确定当前分支名称
                try:
                    branch_name = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=current_dir, capture_output=True, text=True, check=True).stdout.strip()
                except subprocess.CalledProcessError:
                    branch_name = 'main'

                # 检查并创建或切换到main分支
                if branch_name != 'main':
                    try:
                        subprocess.run(['git', 'checkout', 'main'], cwd=current_dir, check=True)
                        branch_name = 'main'
                    except subprocess.CalledProcessError:
                        subprocess.run(['git', 'checkout', '-b', 'main'], cwd=current_dir, check=True)
                        branch_name = 'main'

                # 确保本地分支与远程同步
                try:
                    subprocess.run(['git', 'pull', 'origin', branch_name], cwd=current_dir, check=True)
                except subprocess.CalledProcessError as pull_e:
                    log_debug(f"Warning: Git pull failed: {pull_e}")

                # 推送到GitHub
                log_debug(f"[DEBUG] Pushing to origin/{branch_name}")
                subprocess.run(['git', 'push', 'origin', branch_name], cwd=current_dir, check=True)

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
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip()
            log_debug(f"[ERROR] GitCommandError: {error_msg}")
            return {
                'success': False,
                'message': f'同步失败: {error_msg}',
                'error': error_msg,
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            log_debug(f"[ERROR] General Exception: {str(e)}")
            return {
                'success': False,
                'message': f'同步失败: {str(e)}',
                'error': str(e),
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
            }