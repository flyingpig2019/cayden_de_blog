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
if(guestbookForm) {
    guestbookForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // 获取表单数据
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;
        
        // 这里可以添加表单验证逻辑
        
        // 在实际应用中，这里会发送数据到服务器
        // 但由于我们使用的是静态网站，可以考虑使用GitHub Issues作为评论系统
        // 或者使用第三方评论服务如Disqus
        
        // 显示提交成功消息
        alert(`谢谢您的留言，${name}！\n\n您的留言已收到，我们会尽快回复。`);
        
        // 重置表单
        this.reset();
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