# Cayden的成长博客部署指南

本指南将帮助您将Cayden的成长博客部署到GitHub，并提供两种部署方式：静态网站部署（GitHub Pages）和完整功能部署（需要服务器支持）。

## 部署准备

在开始部署前，请确保您已经：

1. 安装了Git（[下载地址](https://git-scm.com/downloads)）
2. 拥有GitHub账号（[注册地址](https://github.com/join)）
3. 安装了Python 3.9或更高版本

## 方案一：部署静态网站到GitHub Pages（仅前端，无留言功能）

这种方式可以免费托管您的网站，但不支持后端功能（如留言板的数据存储）。

### 步骤1：创建GitHub仓库

1. 登录您的GitHub账号
2. 点击右上角的"+"按钮，选择"New repository"
3. 填写仓库名称（例如：cayden_de_blog）
4. 选择公开（Public）或私有（Private）
5. 点击"Create repository"

### 步骤2：准备静态文件

由于GitHub Pages只支持静态网站，需要使用静态版本的留言板页面：

1. 确保您的项目中包含`static_guestbook.html`文件（已创建）
2. 在导航菜单中，将链接从`guestbook.html`改为`static_guestbook.html`

### 步骤3：初始化Git并推送到GitHub

```bash
# 在项目目录下打开命令行
git init
git add .
git commit -m "初始提交"
git branch -M main
git remote add origin https://github.com/你的用户名/cayden_de_blog.git
git push -u origin main
```

### 步骤4：启用GitHub Pages

1. 在GitHub仓库页面，点击"Settings"
2. 在左侧菜单中找到"Pages"
3. 在"Source"部分，选择"Deploy from a branch"
4. 在"Branch"下拉菜单中选择"main"，文件夹选择"/ (root)"
5. 点击"Save"
6. 等待几分钟，您的网站将在显示的URL上可用（通常是`https://你的用户名.github.io/cayden_de_blog/`）

## 方案二：基于邮件通知的静态留言板（GitHub Pages适用）

这种方式可以在GitHub Pages等静态网站托管平台上实现留言功能，通过第三方服务将留言内容发送到您的邮箱。

### 步骤1：选择第三方表单处理服务

以下是几个推荐的免费服务：

1. **Formspree**（推荐）
   - 注册[Formspree](https://formspree.io/)账号
   - 创建一个新表单
   - 获取表单的提交URL

2. **EmailJS**
   - 注册[EmailJS](https://www.emailjs.com/)账号
   - 设置邮件服务和模板
   - 获取服务ID和模板ID

### 步骤2：修改static_guestbook.html文件

#### 使用Formspree（简单方式）

```html
<!-- 将留言表单部分替换为以下内容 -->
<div class="guestbook-form">
    <h3>给Cayden留言</h3>
    <form action="https://formspree.io/f/您的formspree表单ID" method="POST">
        <div class="form-group">
            <label for="name">您的姓名：</label>
            <input type="text" id="name" name="name" required>
        </div>
        <div class="form-group">
            <label for="email">您的邮箱：</label>
            <input type="email" id="email" name="email" required>
        </div>
        <div class="form-group">
            <label for="message">留言内容：</label>
            <textarea id="message" name="message" rows="4" required></textarea>
        </div>
        <button type="submit" class="btn">提交留言</button>
    </form>
    <p class="form-note">留言将通过邮件发送给博客管理员</p>
</div>
```

#### 使用EmailJS（更多自定义选项）

```html
<!-- 在head部分添加EmailJS库 -->
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/@emailjs/browser@3/dist/email.min.js"></script>

<!-- 将留言表单部分替换为以下内容 -->
<div class="guestbook-form">
    <h3>给Cayden留言</h3>
    <form id="contact-form">
        <div class="form-group">
            <label for="name">您的姓名：</label>
            <input type="text" id="name" name="user_name" required>
        </div>
        <div class="form-group">
            <label for="email">您的邮箱：</label>
            <input type="email" id="email" name="user_email" required>
        </div>
        <div class="form-group">
            <label for="message">留言内容：</label>
            <textarea id="message" name="message" rows="4" required></textarea>
        </div>
        <button type="submit" class="btn">提交留言</button>
    </form>
    <p id="form-status"></p>
</div>

<!-- 在body结束标签前添加以下脚本 -->
<script type="text/javascript">
    (function() {
        emailjs.init('您的EmailJS公钥');
        
        document.getElementById('contact-form').addEventListener('submit', function(event) {
            event.preventDefault();
            document.getElementById('form-status').textContent = '正在发送...'; 
            
            emailjs.sendForm('您的服务ID', '您的模板ID', this)
                .then(function() {
                    document.getElementById('form-status').textContent = '留言已成功发送！';
                    document.getElementById('contact-form').reset();
                }, function(error) {
                    document.getElementById('form-status').textContent = '发送失败，请稍后再试。';
                    console.log('发送失败:', error);
                });
        });
    })();
</script>
```

### 步骤3：更新导航链接

在所有HTML文件中，将导航菜单中的链接从`static_guestbook.html`改回`guestbook.html`，并确保文件名也相应更改。

### 步骤4：部署到GitHub Pages

按照方案一中的步骤部署到GitHub Pages。由于现在留言功能通过第三方服务实现，您的静态网站将能够接收访客留言。

## 方案三：部署完整功能网站（包含数据库留言功能）

这种方式需要一个支持Python的服务器或云平台，以下提供几种选择：

### 选项A：部署到PythonAnywhere（推荐新手使用）

1. 注册[PythonAnywhere](https://www.pythonanywhere.com/)账号（有免费计划）
2. 登录后，点击Dashboard中的"$ Bash"按钮打开命令行
3. 克隆您的GitHub仓库：
   ```
   git clone https://github.com/你的用户名/cayden_de_blog.git
   ```
4. 创建虚拟环境并安装依赖：
   ```
   cd cayden_de_blog
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
5. 在Web选项卡中，点击"Add a new web app"，选择"Manual configuration"和Python 3.9
6. 设置以下配置：
   - Source code: `/home/你的用户名/cayden_de_blog`
   - Working directory: `/home/你的用户名/cayden_de_blog`
   - WSGI configuration file: 编辑此文件，使用以下内容：
     ```python
     import sys
     path = '/home/你的用户名/cayden_de_blog'
     if path not in sys.path:
         sys.path.append(path)
     from app import app as application
     ```
7. 点击"Reload"按钮启动应用

### 选项B：部署到Heroku

1. 注册[Heroku](https://www.heroku.com/)账号
2. 安装[Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
3. 在命令行中登录Heroku：
   ```
   heroku login
   ```
4. 在项目目录中创建Heroku应用：
   ```
   heroku create cayden-blog
   ```
5. 推送代码到Heroku：
   ```
   git push heroku main
   ```
6. 打开应用：
   ```
   heroku open
   ```

## 数据库注意事项

默认情况下，SQLite数据库文件（`data/guestbook.db`）不会被提交到Git仓库（已在.gitignore中配置）。如果您希望保留现有留言数据，有以下选择：

1. 修改.gitignore文件，取消对数据库文件的排除
2. 使用数据库迁移脚本备份和恢复数据
3. 对于生产环境，考虑使用更强大的数据库如PostgreSQL或MySQL

## 更新网站

当您对网站进行更改后，可以通过以下命令更新部署：

```bash
git add .
git commit -m "更新网站内容"
git push origin main
```

对于GitHub Pages，更改将在几分钟内自动生效。对于其他平台，可能需要额外的部署步骤。

## 常见问题

1. **GitHub Pages上留言功能不工作**
   - 这是正常的，GitHub Pages只支持静态网站，不支持后端数据库功能。您可以使用方案二（基于邮件通知的静态留言板）或方案三（完整功能部署）来解决这个问题。

2. **使用Formspree时收到垃圾邮件怎么办？**
   - Formspree提供了垃圾邮件过滤功能，您可以在Formspree控制面板中设置过滤规则。
   - 考虑添加验证码（如reCAPTCHA）到您的表单中。

3. **如何自定义邮件通知的内容？**
   - 使用Formspree时，可以在控制面板中自定义邮件模板。
   - 使用EmailJS时，可以在EmailJS控制面板中创建和编辑邮件模板。

2. **如何更改域名？**
   - 对于GitHub Pages，可以在仓库设置中的Pages部分配置自定义域名。
   - 对于其他平台，请参考各平台的域名设置文档。

3. **数据库文件丢失怎么办？**
   - 如果您没有备份数据库，可能需要重新创建。应用程序会在启动时自动创建空数据库。

## 获取帮助

如果您在部署过程中遇到问题，可以：

1. 查阅[GitHub Pages文档](https://docs.github.com/cn/pages)
2. 查阅您选择的部署平台的文档
3. 在GitHub上创建Issue寻求帮助