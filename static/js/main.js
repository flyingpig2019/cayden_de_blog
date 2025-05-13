// 当前语言，默认为中文
let currentLang = localStorage.getItem('language') || 'zh';

// 管理员登录状态
let isAdminLoggedIn = false;

// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 初始化语言切换按钮
    initLanguageSwitcher();
    
    // 初始化管理员登录
    initAdminLogin();
    
    // 应用当前语言
    applyLanguage(currentLang);
    // 照片墙筛选功能
    const filterButtons = document.querySelectorAll('.filter-btn');
    const photoItems = document.querySelectorAll('.photo-item');
    
    if(filterButtons.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                // 移除所有按钮的active类
                filterButtons.forEach(btn => btn.classList.remove('active'));
                // 给当前点击的按钮添加active类
                this.classList.add('active');
                
                const filter = this.getAttribute('data-filter');
                
                photoItems.forEach(item => {
                    if(filter === 'all' || item.getAttribute('data-category') === filter) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                });
            });
        });
    }
    
    // 为Lightbox设置选项
    if(typeof lightbox !== 'undefined') {
        lightbox.option({
            'resizeDuration': 200,
            'wrapAround': true,
            'albumLabel': "图片 %1 / %2"
        });
    }
    
    // 处理详情按钮点击事件
    // 新增按钮点击处理
    document.querySelectorAll('a[data-target="detail"]').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('查看详情：' + this.closest('.featured-item').querySelector('h3').textContent);
        });
    });

    // 平滑滚动到锚点
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if(targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if(targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // 初始化管理员面板（如果已登录）
    checkAdminLoginStatus();
    
    console.log('网站已加载完成');
});

// 留言板表单提交处理
const guestbookForm = document.getElementById('guestbook-form');
const messagesContainer = document.getElementById('messages-container');

// 加载留言数据
function loadMessages() {
    if(messagesContainer) {
        messagesContainer.innerHTML = '<div class="loading-messages">正在加载留言...</div>';
        
        fetch('/api/messages')
            .then(response => response.json())
            .then(messages => {
                if(messages.length === 0) {
                    messagesContainer.innerHTML = '<p class="no-messages">暂无留言，快来留下第一条吧！</p>';
                    return;
                }
                
                let html = '';
                messages.forEach(msg => {
                    const date = new Date(msg.created_at).toLocaleString('zh-CN');
                    html += `
                        <div class="comment">
                            <div class="comment-header">
                                <span class="comment-author">${msg.name}</span>
                                <span class="comment-date">${date}</span>
                            </div>
                            <div class="comment-content">${msg.message}</div>
                        </div>
                    `;
                });
                
                messagesContainer.innerHTML = html;
            })
            .catch(error => {
                console.error('获取留言失败:', error);
                messagesContainer.innerHTML = '<p class="error-message">获取留言失败，请稍后再试。</p>';
            });
    }
}

// 页面加载时获取留言
if(messagesContainer) {
    loadMessages();
}

// 提交留言表单
if(guestbookForm) {
    guestbookForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // 获取表单数据
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;
        
        // 简单的表单验证
        if(!name || !email || !message) {
            alert('请填写所有必填字段！');
            return;
        }
        
        // 禁用提交按钮，防止重复提交
        const submitBtn = this.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = '提交中...';
        
        // 发送数据到服务器
        fetch('/api/messages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, email, message })
        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                alert(`谢谢您的留言，${name}！\n\n您的留言已成功提交。`);
                this.reset();
                // 重新加载留言列表
                loadMessages();
            } else {
                alert('留言提交失败：' + (data.error || '未知错误'));
            }
        })
        .catch(error => {
            console.error('提交留言失败:', error);
            alert('提交留言失败，请稍后再试。');
        })
        .finally(() => {
            // 恢复提交按钮
            submitBtn.disabled = false;
            submitBtn.textContent = '提交留言';
        });
    });
}

// 响应式导航菜单
const createMobileMenu = () => {
    const nav = document.querySelector('nav');
    if(!nav) return;
    
    const mobileMenuBtn = document.createElement('button');
    mobileMenuBtn.className = 'mobile-menu-btn';
    mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>';
    
    nav.querySelector('.container').prepend(mobileMenuBtn);
    
    mobileMenuBtn.addEventListener('click', function() {
        nav.classList.toggle('mobile-menu-open');
    });
};

// 检测屏幕宽度，在小屏幕上创建移动菜单
if(window.innerWidth < 768) {
    createMobileMenu();
}

// 监听窗口大小变化
window.addEventListener('resize', function() {
    if(window.innerWidth < 768) {
        if(!document.querySelector('.mobile-menu-btn')) {
            createMobileMenu();
        }
    }
});

// 语言切换功能
function initLanguageSwitcher() {
    // 创建语言切换按钮
    const header = document.querySelector('header .container');
    if(!header) return;
    
    const langSwitcher = document.createElement('div');
    langSwitcher.className = 'lang-switcher';
    langSwitcher.innerHTML = `
        <button class="lang-btn ${currentLang === 'zh' ? 'active' : ''}" data-lang="zh">中文</button>
        <span>/</span>
        <button class="lang-btn ${currentLang === 'en' ? 'active' : ''}" data-lang="en">ENG</button>
    `;
    
    header.appendChild(langSwitcher);
    
    // 添加语言切换事件
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const lang = this.getAttribute('data-lang');
            currentLang = lang;
            localStorage.setItem('language', lang);
            
            // 更新按钮状态
            document.querySelectorAll('.lang-btn').forEach(b => {
                b.classList.remove('active');
            });
            this.classList.add('active');
            
            // 应用语言
            applyLanguage(lang);
        });
    });
}

// 应用语言到页面元素
function applyLanguage(lang) {
    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(el => {
        const key = el.getAttribute('data-i18n');
        if(translations[lang] && translations[lang][key]) {
            el.textContent = translations[lang][key];
        }
    });
    
    // 更新页面标题
    document.title = lang === 'zh' ? 'Cayden的成长博客' : 'Cayden\'s Growth Blog';
    
    // 更新表单占位符
    const placeholders = document.querySelectorAll('[data-i18n-placeholder]');
    placeholders.forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if(translations[lang] && translations[lang][key]) {
            el.placeholder = translations[lang][key];
        }
    });
}

// 管理员登录功能
function initAdminLogin() {
    // 创建管理员登录按钮
    const nav = document.querySelector('nav .container ul');
    if(!nav) return;
    
    const adminLoginLi = document.createElement('li');
    adminLoginLi.className = 'admin-login-item';
    adminLoginLi.innerHTML = `<a href="#" id="admin-login-btn" data-i18n="admin_login">管理员登录</a>`;
    
    nav.appendChild(adminLoginLi);
    
    // 创建登录模态框
    const loginModal = document.createElement('div');
    loginModal.className = 'modal';
    loginModal.id = 'login-modal';
    loginModal.innerHTML = `
        <div class="modal-content">
            <span class="close">&times;</span>
            <h2 data-i18n="admin_login">管理员登录</h2>
            <form id="admin-login-form">
                <div class="form-group">
                    <label for="admin-email" data-i18n="email">邮箱</label>
                    <input type="email" id="admin-email" data-i18n-placeholder="email_placeholder" placeholder="请输入邮箱" required>
                </div>
                <div class="form-group">
                    <label for="admin-password" data-i18n="password">密码</label>
                    <input type="password" id="admin-password" data-i18n-placeholder="password_placeholder" placeholder="请输入密码" required>
                </div>
                <button type="submit" class="btn" data-i18n="login">登录</button>
            </form>
        </div>
    `;
    
    document.body.appendChild(loginModal);
    
    // 添加登录按钮点击事件
    document.getElementById('admin-login-btn').addEventListener('click', function(e) {
        e.preventDefault();
        document.getElementById('login-modal').style.display = 'block';
    });
    
    // 关闭模态框
    document.querySelector('#login-modal .close').addEventListener('click', function() {
        document.getElementById('login-modal').style.display = 'none';
    });
    
    // 点击模态框外部关闭
    window.addEventListener('click', function(e) {
        if(e.target === document.getElementById('login-modal')) {
            document.getElementById('login-modal').style.display = 'none';
        }
    });
    
    // 处理登录表单提交
    document.getElementById('admin-login-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const email = document.getElementById('admin-email').value;
        const password = document.getElementById('admin-password').value;
        
        // 验证管理员账号
        if(email === 'grand.cayden@gmail.com' && password === 'Cayden@2019') {
            // 登录成功
            isAdminLoggedIn = true;
            localStorage.setItem('adminLoggedIn', 'true');
            
            // 关闭登录模态框
            document.getElementById('login-modal').style.display = 'none';
            
            // 更新UI显示管理员面板
            updateAdminUI();
            
            // 显示管理员面板
            showAdminPanel();
        } else {
            // 登录失败
            alert(translations[currentLang]['login_error']);
        }
    });
}

// 检查管理员登录状态
function checkAdminLoginStatus() {
    if(localStorage.getItem('adminLoggedIn') === 'true') {
        isAdminLoggedIn = true;
        updateAdminUI();
    }
}

// 更新管理员UI
function updateAdminUI() {
    const adminLoginBtn = document.getElementById('admin-login-btn');
    if(adminLoginBtn) {
        if(isAdminLoggedIn) {
            adminLoginBtn.textContent = translations[currentLang]['admin_panel'];
            adminLoginBtn.setAttribute('data-i18n', 'admin_panel');
            adminLoginBtn.removeEventListener('click', showLoginModal);
            adminLoginBtn.addEventListener('click', showAdminPanel);
        } else {
            adminLoginBtn.textContent = translations[currentLang]['admin_login'];
            adminLoginBtn.setAttribute('data-i18n', 'admin_login');
        }
    }
}

// 显示登录模态框
function showLoginModal(e) {
    if(e) e.preventDefault();
    document.getElementById('login-modal').style.display = 'block';
}

// 显示管理员面板
function showAdminPanel(e) {
    if(e) e.preventDefault();
    
    // 如果管理员面板不存在，创建它
    if(!document.getElementById('admin-panel')) {
        createAdminPanel();
    }
    
    document.getElementById('admin-panel').style.display = 'block';
}

// 创建管理员面板
function createAdminPanel() {
    const adminPanel = document.createElement('div');
    adminPanel.className = 'modal';
    adminPanel.id = 'admin-panel';
    adminPanel.innerHTML = `
        <div class="modal-content admin-panel-content">
            <span class="close">&times;</span>
            <h2 data-i18n="admin_panel">管理员面板</h2>
            
            <div class="admin-tabs">
                <button class="tab-btn active" data-tab="upload-photo" data-i18n="upload_photo">上传照片</button>
                <button class="tab-btn" data-tab="add-video" data-i18n="add_video">添加视频</button>
                <button id="admin-logout-btn" class="btn logout-btn" data-i18n="logout">退出</button>
            </div>
            
            <div class="tab-content" id="upload-photo-tab">
                <form id="upload-photo-form">
                    <div class="form-group">
                        <label for="photo-title" data-i18n="photo_title">照片标题</label>
                        <input type="text" id="photo-title" required>
                    </div>
                    <div class="form-group">
                        <label for="photo-category" data-i18n="photo_category">照片分类</label>
                        <select id="photo-category">
                            <option value="school">学校生活</option>
                            <option value="family">家庭活动</option>
                            <option value="travel">旅行记忆</option>
                            <option value="hobby">兴趣爱好</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="photo-file">照片文件</label>
                        <input type="file" id="photo-file" accept="image/*" required>
                    </div>
                    <button type="submit" class="btn" data-i18n="upload">上传</button>
                </form>
            </div>
            
            <div class="tab-content" id="add-video-tab" style="display: none;">
                <form id="add-video-form">
                    <div class="form-group">
                        <label for="video-title" data-i18n="video_title">视频标题</label>
                        <input type="text" id="video-title" required>
                    </div>
                    <div class="form-group">
                        <label for="video-url" data-i18n="video_url">YouTube视频链接</label>
                        <input type="url" id="video-url" required>
                    </div>
                    <button type="submit" class="btn" data-i18n="add">添加</button>
                </form>
            </div>
        </div>
    `;
    
    document.body.appendChild(adminPanel);
    
    // 关闭面板
    document.querySelector('#admin-panel .close').addEventListener('click', function() {
        document.getElementById('admin-panel').style.display = 'none';
    });
    
    // 点击面板外部关闭
    window.addEventListener('click', function(e) {
        if(e.target === document.getElementById('admin-panel')) {
            document.getElementById('admin-panel').style.display = 'none';
        }
    });
    
    // 标签切换
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            if(this.id === 'admin-logout-btn') return;
            
            // 更新按钮状态
            document.querySelectorAll('.tab-btn').forEach(b => {
                b.classList.remove('active');
            });
            this.classList.add('active');
            
            // 显示对应内容
            const tabId = this.getAttribute('data-tab');
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.style.display = 'none';
            });
            document.getElementById(tabId + '-tab').style.display = 'block';
        });
    });
    
    // 退出登录
    document.getElementById('admin-logout-btn').addEventListener('click', function() {
        isAdminLoggedIn = false;
        localStorage.removeItem('adminLoggedIn');
        document.getElementById('admin-panel').style.display = 'none';
        updateAdminUI();
    });
    
    // 处理照片上传
    document.getElementById('upload-photo-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        // 这里应该有实际的上传逻辑，但由于是前端演示，我们只模拟成功
        alert(translations[currentLang]['upload_success']);
        this.reset();
    });
    
    // 处理视频添加
    document.getElementById('add-video-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        // 这里应该有实际的添加逻辑，但由于是前端演示，我们只模拟成功
        alert(translations[currentLang]['add_success']);
        this.reset();
    });
    
    // 应用当前语言
    applyLanguage(currentLang);
}