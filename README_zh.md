# 凯登的成长博客

一个使用Flask构建的个人博客应用，用于记录凯登的成长历程。该应用包括照片画廊、视频集合、带有日历集成的成长故事以及访客留言板。

## 功能特点

- **多语言支持**：在英语和中文之间切换
- **照片画廊**：上传和管理照片
- **视频集合**：嵌入和管理视频
- **成长故事**：基于日历的成长历程记录
- **留言板**：允许访客留言并由管理员回复
- **管理员仪表板**：用于内容管理的安全管理区域
- **内联编辑**：以管理员身份登录时直接在页面上编辑内容

## 项目结构

```
/cayden_blog/
│
├── app.py                 # 主Flask应用
├── schema.sql             # 数据库模式
├── requirements.txt       # 依赖项
├── .env                   # 环境变量
├── babel.cfg              # Babel翻译配置
│
├── templates/             # HTML模板
│   ├── base.html          # 包含页眉、页脚等的基础模板
│   ├── index.html         # 首页
│   ├── photos.html        # 照片画廊
│   ├── videos.html        # 视频集合
│   ├── growth.html        # 带有日历的成长故事
│   ├── messages.html      # 留言板
│   ├── admin.html         # 管理员仪表板
│   └── login.html         # 管理员登录
│
├── static/
│   ├── css/
│   │   └── style.css      # 主样式表
│   ├── js/
│   │   ├── main.js        # 主JavaScript文件
│   │   └── admin.js       # 管理员特定JavaScript
│   └── uploads/           # 上传的图片
│
└── translations/          # 语言翻译（生成的）
```

## 安装说明

### 前提条件

- Python 3.7或更高版本
- pip（Python包管理器）

### 安装

1. 克隆仓库或下载源代码

2. 导航到项目目录

3. 创建虚拟环境（推荐）：
   ```
   python -m venv venv
   ```

4. 激活虚拟环境：
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

5. 安装依赖项：
   ```
   pip install -r requirements.txt
   ```

6. 初始化数据库：
   ```
   flask init-db
   ```

7. 运行应用：
   ```
   flask run
   ```

8. 在浏览器中访问应用：`http://127.0.0.1:5000`

### 管理员访问

使用以下凭据登录为管理员：
- 电子邮件：您在.env文件中指定的电子邮件（默认：grand.cayden@gmail.com）
- 认证码：如果配置了TOTP，则需要输入可选的TOTP代码

## 翻译管理

提取要翻译的消息：

```
pybabel extract -F babel.cfg -o messages.pot .
pybabel init -i messages.pot -d translations -l zh
```

编辑`translations/zh/LC_MESSAGES/messages.po`中的翻译文件

编译翻译：

```
pybabel compile -d translations
```

## 许可证

本项目仅供个人使用。

## 支持

如有任何问题或疑问，请联系管理员。