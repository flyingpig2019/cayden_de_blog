// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
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
    
    // 创建占位图片文件夹
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