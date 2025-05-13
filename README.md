# Cayden的成长博客

这是一个记录和分享6岁小朋友Cayden成长历程的个人博客网站。网站包含照片墙、视频集、成长故事和留言板等功能。

## 网站功能

- **首页**：展示网站概览和精选内容
- **照片墙**：按分类展示Cayden的照片，支持筛选和灯箱效果
- **视频集**：收集和展示Cayden的视频记录
- **成长故事**：记录Cayden生活中的点滴和成长经历
- **留言板**：访客可以留言互动，支持三种实现方式：
  - 基于SQLite数据库的完整留言功能
  - 基于Formspree的邮件通知留言板（适用于静态网站）
  - 基于EmailJS的邮件通知留言板（适用于静态网站）

## 技术栈

- **前端技术**：HTML5, CSS3, JavaScript
- **后端技术**：Python Flask
- **数据管理**：SQLite数据库
- **静态资源**：图片、CSS和JavaScript文件

## 如何运行

### 本地运行

1. 克隆仓库到本地
   ```
   git clone https://github.com/你的用户名/cayden_de_blog.git
   cd cayden_de_blog
   ```

2. 安装依赖
   ```
   pip install -r requirements.txt
   ```

3. 运行应用
   ```
   python app.py
   ```

4. 在浏览器中访问 `http://127.0.0.1:8000`

### 部署到GitHub

1. 在GitHub上创建新仓库
   - 登录GitHub账号
   - 点击右上角的"+"按钮，选择"New repository"
   - 填写仓库名称（例如：cayden_de_blog）
   - 选择公开或私有
   - 点击"Create repository"

2. 初始化本地Git仓库并推送到GitHub
   ```
   git init
   git add .
   git commit -m "初始提交"
   git branch -M main
   git remote add origin https://github.com/你的用户名/cayden_de_blog.git
   git push -u origin main
   ```

3. 设置GitHub Pages（静态网站部分）
   - 在GitHub仓库页面，点击"Settings"
   - 滚动到"GitHub Pages"部分
   - 在"Source"下拉菜单中选择"main"分支
   - 点击"Save"
   - 等待几分钟后，您的网站将在显示的URL上可用

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动服务器

```bash
python app.py
```

服务器将在 http://localhost:8000 启动，可以通过浏览器访问。

### 数据库说明

留言板功能使用SQLite数据库存储用户留言，数据保存在`data/guestbook.db`文件中。首次运行时，系统会自动创建数据库和表结构。

## 如何更新内容

### 添加新照片

1. 将照片文件放入`static/images`目录
2. 在`photos.html`文件中按照现有格式添加新的照片项

### 添加新视频

1. 将视频上传至YouTube或其他视频平台
2. 在`videos.html`文件中按照现有格式添加新的视频嵌入代码

### 添加新故事

在`stories.html`文件中按照现有格式添加新的故事内容

## 留言板功能

留言板功能提供三种实现方式：

### 1. 基于SQLite数据库的完整留言功能

- 用户可以提交姓名、邮箱和留言内容
- 留言会实时显示在页面上
- 所有留言按时间倒序排列
- 数据安全存储在SQLite数据库中
- 需要服务器支持（如PythonAnywhere或Heroku）

### 2. 基于邮件通知的静态留言板

- 适用于GitHub Pages等静态网站托管平台
- 支持两种实现方式：
  - **Formspree实现**：简单易用，无需JavaScript知识
  - **EmailJS实现**：提供更多自定义选项
- 用户提交的留言将通过邮件发送给网站管理员
- 示例文件：`formspree_guestbook.html`和`email_guestbook.html`

## 项目结构

- `app.py` - Flask应用主文件
- `index.html` - 网站首页
- `photos.html` - 照片墙页面
- `videos.html` - 视频集页面
- `stories.html` - 成长故事页面
- `guestbook.html` - 数据库版留言板页面
- `static_guestbook.html` - 静态版留言板页面（无功能）
- `email_guestbook.html` - 基于EmailJS的邮件通知留言板
- `formspree_guestbook.html` - 基于Formspree的邮件通知留言板
- `DEPLOYMENT_GUIDE.md` - 部署指南文档
- `static/` - 静态资源目录
  - `css/` - CSS样式文件
  - `js/` - JavaScript脚本文件
  - `images/` - 图片资源
- `data/` - 数据目录（自动创建）
  - `guestbook.db` - SQLite数据库文件

## 注意事项

- 所有图片文件应放在`static/images`目录下
- 为保护隐私，建议不要在公开网站上使用真实照片，可以使用处理过的或示意性图片
- 定期备份数据库文件`data/guestbook.db`以防数据丢失
- 默认端口为8000，可以在`app.py`中修改

## 许可证

本项目采用MIT许可证。

---

祝你使用愉快！如有任何问题，请联系我。