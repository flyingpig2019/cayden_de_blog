# Cayden的成长博客

这是一个基于GitHub Pages的静态个人博客网站，专门用于记录和分享6岁小朋友Cayden的成长历程。网站包含照片墙、视频集、成长故事和留言板等功能。

## 网站功能

- **首页**：展示网站概览和精选内容
- **照片墙**：按分类展示Cayden的照片，支持筛选和灯箱效果
- **视频集**：收集和展示Cayden的视频记录
- **成长故事**：记录Cayden生活中的点滴和成长经历
- **留言板**：访客可以留言互动，集成Disqus评论系统

## 技术栈

- **托管平台**：GitHub Pages
- **前端技术**：HTML5, CSS3, JavaScript
- **数据管理**：静态HTML和JSON
- **评论系统**：Disqus

## 如何部署

### 部署到GitHub Pages

1. 在GitHub上创建一个新的仓库，命名为`username.github.io`（将`username`替换为你的GitHub用户名）
2. 将本项目所有文件上传到该仓库
3. 在仓库设置中启用GitHub Pages功能
4. 几分钟后，你的网站将可以通过`https://username.github.io`访问

### 自定义域名（可选）

1. 在你的域名提供商处添加一条CNAME记录，指向`username.github.io`
2. 在GitHub仓库中创建一个名为`CNAME`的文件，内容为你的自定义域名
3. 在仓库设置的GitHub Pages部分配置自定义域名

## 如何更新内容

### 添加新照片

1. 将照片文件放入`static/images`目录
2. 在`photos.html`文件中按照现有格式添加新的照片项

### 添加新视频

1. 将视频上传至YouTube或其他视频平台
2. 在`videos.html`文件中按照现有格式添加新的视频嵌入代码

### 添加新故事

在`stories.html`文件中按照现有格式添加新的故事内容

## 评论系统配置

本网站使用Disqus作为评论系统。要配置Disqus：

1. 注册Disqus账号并创建一个站点
2. 获取Disqus的通用代码
3. 将代码中的`s.src`值中的`cayden-blog`替换为你的Disqus站点名称

## 注意事项

- 所有图片文件应放在`static/images`目录下
- 为保护隐私，建议不要在公开网站上使用真实照片，可以使用处理过的或示意性图片
- 定期备份网站内容

## 许可证

本项目采用MIT许可证。详见[LICENSE](LICENSE)文件。

---

祝你使用愉快！如有任何问题，请通过GitHub Issues联系我。