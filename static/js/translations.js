// 多语言翻译文件
const translations = {
    'zh': {
        // 导航
        'nav_home': '首页',
        'nav_photos': '照片墙',
        'nav_videos': '视频集',
        'nav_stories': '成长故事',
        'nav_guestbook': '留言板',
        
        // 首页
        'welcome_title': '欢迎来到Cayden的小天地',
        'welcome_desc': '这里记录着Cayden成长的每一个精彩瞬间，分享他的笑容、故事和点滴进步。',
        'featured_moments': '精彩瞬间',
        'first_school_day': '第一次上学',
        'first_school_day_desc': 'Cayden第一天上学的照片，他看起来既兴奋又有点紧张。',
        'birthday_party': '六岁生日派对',
        'birthday_party_desc': '和朋友们一起庆祝六岁生日的欢乐时光。',
        'first_bike': '第一次骑自行车',
        'first_bike_desc': 'Cayden学会骑自行车的那一刻，脸上洋溢着自豪的笑容。',
        'view_details': '查看详情',
        'recent_stories': '最新故事',
        'read_more': '阅读全文',
        
        // 照片墙
        'photo_wall': 'Cayden的照片墙',
        'photo_wall_desc': '记录每一个珍贵的瞬间，定格成长的足迹',
        'photo_categories': '照片分类',
        'all': '全部',
        'school_life': '学校生活',
        'family_activities': '家庭活动',
        'travel_memories': '旅行记忆',
        'hobbies': '兴趣爱好',
        
        // 留言板
        'guestbook': '留言板',
        'guestbook_desc': '欢迎留下您的祝福和鼓励',
        'name': '姓名',
        'email': '邮箱',
        'message': '留言',
        'submit': '提交留言',
        'loading_messages': '正在加载留言...',
        'no_messages': '暂无留言，快来留下第一条吧！',
        'submit_success': '谢谢您的留言，{name}！\n\n您的留言已成功提交。',
        'submit_error': '留言提交失败：',
        'fill_all_fields': '请填写所有必填字段！',
        'submitting': '提交中...',
        
        // 管理员
        'admin_login': '管理员登录',
        'login': '登录',
        'logout': '退出',
        'email_placeholder': '请输入邮箱',
        'password_placeholder': '请输入密码',
        'login_error': '登录失败，请检查邮箱和密码',
        'admin_panel': '管理面板',
        'upload_photo': '上传照片',
        'add_video': '添加视频',
        'photo_title': '照片标题',
        'photo_category': '照片分类',
        'video_title': '视频标题',
        'video_url': 'YouTube视频链接',
        'upload': '上传',
        'add': '添加',
        'upload_success': '上传成功！',
        'add_success': '添加成功！'
    },
    'en': {
        // Navigation
        'nav_home': 'Home',
        'nav_photos': 'Photos',
        'nav_videos': 'Videos',
        'nav_stories': 'Stories',
        'nav_guestbook': 'Guestbook',
        
        // Home page
        'welcome_title': 'Welcome to Cayden\'s World',
        'welcome_desc': 'Here we record every wonderful moment of Cayden\'s growth, sharing his smiles, stories, and progress.',
        'featured_moments': 'Featured Moments',
        'first_school_day': 'First Day at School',
        'first_school_day_desc': 'Cayden\'s first day at school, he looks both excited and a bit nervous.',
        'birthday_party': '6th Birthday Party',
        'birthday_party_desc': 'Happy times celebrating his 6th birthday with friends.',
        'first_bike': 'First Time Riding a Bike',
        'first_bike_desc': 'The moment Cayden learned to ride a bike, his face was full of pride.',
        'view_details': 'View Details',
        'recent_stories': 'Recent Stories',
        'read_more': 'Read More',
        
        // Photo wall
        'photo_wall': 'Cayden\'s Photo Wall',
        'photo_wall_desc': 'Recording every precious moment, freezing the footprints of growth',
        'photo_categories': 'Photo Categories',
        'all': 'All',
        'school_life': 'School Life',
        'family_activities': 'Family Activities',
        'travel_memories': 'Travel Memories',
        'hobbies': 'Hobbies',
        
        // Guestbook
        'guestbook': 'Guestbook',
        'guestbook_desc': 'Welcome to leave your blessings and encouragement',
        'name': 'Name',
        'email': 'Email',
        'message': 'Message',
        'submit': 'Submit',
        'loading_messages': 'Loading messages...',
        'no_messages': 'No messages yet, be the first to leave one!',
        'submit_success': 'Thank you for your message, {name}!\n\nYour message has been submitted successfully.',
        'submit_error': 'Failed to submit message: ',
        'fill_all_fields': 'Please fill in all required fields!',
        'submitting': 'Submitting...',
        
        // Admin
        'admin_login': 'Admin Login',
        'login': 'Login',
        'logout': 'Logout',
        'email_placeholder': 'Enter email',
        'password_placeholder': 'Enter password',
        'login_error': 'Login failed, please check email and password',
        'admin_panel': 'Admin Panel',
        'upload_photo': 'Upload Photo',
        'add_video': 'Add Video',
        'photo_title': 'Photo Title',
        'photo_category': 'Photo Category',
        'video_title': 'Video Title',
        'video_url': 'YouTube Video URL',
        'upload': 'Upload',
        'add': 'Add',
        'upload_success': 'Upload successful!',
        'add_success': 'Added successfully!'
    }
};

// 导出翻译对象
if (typeof module !== 'undefined' && module.exports) {
    module.exports = translations;
}