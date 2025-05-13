# Cayden的成长博客

这是一个记录和分享6岁小朋友Cayden成长历程的个人博客网站。网站包含照片墙、视频集、成长故事和留言板等功能。

## 网站功能

- **首页**：展示网站概览和精选内容
- **照片墙**：按分类展示Cayden的照片，支持筛选和灯箱效果
- **视频集**：收集和展示Cayden的视频记录
- **成长故事**：记录Cayden生活中的点滴和成长经历
- **留言板**：访客可以留言互动，使用SQLite数据库存储留言

## 技术栈

- **前端技术**：HTML5, CSS3, JavaScript
- **后端技术**：Python Flask
- **数据管理**：SQLite数据库
- **静态资源**：图片、CSS和JavaScript文件

## 如何运行

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

留言板功能使用SQLite数据库存储用户留言。主要特点：

1. 用户可以提交姓名、邮箱和留言内容
2. 留言会实时显示在页面上
3. 所有留言按时间倒序排列
4. 数据安全存储在SQLite数据库中

## 项目结构

- `app.py` - Flask应用主文件
- `index.html` - 网站首页
- `photos.html` - 照片墙页面
- `videos.html` - 视频集页面
- `stories.html` - 成长故事页面
- `guestbook.html` - 留言板页面
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