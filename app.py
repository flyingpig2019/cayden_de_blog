import os
import sqlite3
import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, g, jsonify, make_response, send_from_directory
from flask_babel import Babel, gettext as _
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import pyotp

# Load environment variables
load_dotenv()

# App configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# 修改上传文件夹路径，确保一致性
upload_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = upload_folder
print(f"Upload folder configured as: {upload_folder}")
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['DATABASE'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')
app.config['SESSION_DURATION'] = int(os.getenv('SESSION_DURATION', 7))

# Babel configuration for multilingual support
babel = Babel(app)

# Custom template filter for datetime formatting
@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d'):
    if isinstance(value, str):
        try:
            dt = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            return dt.strftime(format)
        except ValueError:
            return value
    return value

@babel.localeselector
def get_locale():
    # Get locale from session or default to English
    return session.get('locale', 'en')

# Database functions
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()

def init_db():
    """Initialize the database with the required tables"""
    db = get_db()
    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    db.commit()

@app.cli.command('init-db')
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    print('Initialized the database.')

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session or not session['admin_logged_in']:
            flash(_('Please log in to access this page'), 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Routes
@app.route('/')
def index():
    db = get_db()
    content = db.execute('SELECT content FROM page_content WHERE page_name = ?', ('index',)).fetchone()
    if content is None:
        content = {'content': _('Welcome to Cayden\'s Growth Blog!')}
    # Add cache control headers to prevent browser caching
    response = make_response(render_template('index.html', content=content['content']))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/photos')
def photos():
    db = get_db()
    photos = db.execute('SELECT *, datetime(uploaded_at) as uploaded_at FROM photo ORDER BY uploaded_at DESC').fetchall()
    # Add cache control headers to prevent browser caching
    response = make_response(render_template('photos.html', photos=photos))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/videos')
def videos():
    db = get_db()
    videos = db.execute('SELECT * FROM video ORDER BY uploaded_at DESC').fetchall()
    # Add cache control headers to prevent browser caching
    response = make_response(render_template('videos.html', videos=videos))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/growth')
def growth():
    db = get_db()
    stories = db.execute('SELECT * FROM growth_story ORDER BY entry_date DESC').fetchall()
    # Add cache control headers to prevent browser caching
    response = make_response(render_template('growth.html', stories=stories))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/messages')
def messages():
    db = get_db()
    messages = db.execute('SELECT * FROM message ORDER BY created_at DESC').fetchall()
    # Add cache control headers to prevent browser caching
    response = make_response(render_template('messages.html', messages=messages))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

# Admin login/logout routes
@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        totp_code = request.form.get('totp_code')
        
        # Verify email
        if email != os.getenv('ADMIN_EMAIL'):
            flash(_('Invalid email'), 'error')
            return redirect(url_for('login'))
        
        # Verify TOTP if provided
        totp_secret = os.getenv('TOTP_SECRET')
        if totp_secret and totp_code:
            totp = pyotp.TOTP(totp_secret)
            if not totp.verify(totp_code):
                flash(_('Invalid authentication code'), 'error')
                return redirect(url_for('login'))
        
        # Set session
        session['admin_logged_in'] = True
        session['admin_email'] = email
        session.permanent = True
        app.permanent_session_lifetime = datetime.timedelta(days=app.config['SESSION_DURATION'])
        
        flash(_('Logged in successfully'), 'success')
        return redirect(url_for('admin'))
    
    return render_template('login.html')

@app.route('/admin/logout')
def logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_email', None)
    flash(_('Logged out successfully'), 'success')
    return redirect(url_for('index'))

# Language toggle
@app.route('/set_language/<language>')
def set_language(language):
    session['locale'] = language
    return redirect(request.referrer or url_for('index'))

# API endpoints for inline editing
@app.route('/api/update_content', methods=['POST'])
@login_required
def update_content():
    data = request.json
    page_name = data.get('page_name')
    content = data.get('content')
    
    if not page_name or not content:
        return jsonify({'success': False, 'message': _('Missing required fields')})
    
    db = get_db()
    db.execute(
        'INSERT OR REPLACE INTO page_content (page_name, content, last_updated) VALUES (?, ?, ?)',
        (page_name, content, datetime.datetime.now())
    )
    db.commit()
    
    return jsonify({'success': True, 'message': _('Content updated successfully')})

@app.route('/api/add_photo', methods=['POST'])
@login_required
def add_photo():
    if 'photo' not in request.files:
        return jsonify({'success': False, 'message': _('No file part')})
    
    file = request.files['photo']
    description = request.form.get('description', '')
    
    if file.filename == '':
        return jsonify({'success': False, 'message': _('No selected file')})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Ensure upload folder exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        db = get_db()
        db.execute(
            'INSERT INTO photo (filename, description, uploaded_at) VALUES (?, ?, ?)',
            (filename, description, datetime.datetime.now())
        )
        db.commit()
        
        return jsonify({'success': True, 'message': _('Photo uploaded successfully')})
    
    return jsonify({'success': False, 'message': _('File type not allowed')})

@app.route('/api/add_video', methods=['POST'])
@login_required
def add_video():
    data = request.json
    embed_url = data.get('embed_url')
    description = data.get('description', '')
    
    if not embed_url:
        return jsonify({'success': False, 'message': _('Missing embed URL')})
    
    # 处理YouTube链接，包括短链接格式
    from utils import convert_youtube_url
    embed_url = convert_youtube_url(embed_url)
    
    db = get_db()
    db.execute(
        'INSERT INTO video (embed_url, description, uploaded_at) VALUES (?, ?, ?)',
        (embed_url, description, datetime.datetime.now())
    )
    db.commit()
    
    return jsonify({'success': True, 'message': _('Video added successfully')})

@app.route('/api/add_growth_story', methods=['POST'])
@login_required
def add_growth_story():
    data = request.json
    entry_date = data.get('entry_date')
    content = data.get('content')
    image = data.get('image', '')
    
    if not entry_date or not content:
        return jsonify({'success': False, 'message': _('Missing required fields')})
    
    db = get_db()
    db.execute(
        'INSERT OR REPLACE INTO growth_story (entry_date, content, image) VALUES (?, ?, ?)',
        (entry_date, content, image)
    )
    db.commit()
    
    return jsonify({'success': True, 'message': _('Growth story added successfully')})

@app.route('/api/public_add_message', methods=['POST'])
def public_add_message():
    data = request.json
    user_name = data.get('user_name')
    content = data.get('content')
    
    if not user_name or not content:
        return jsonify({'success': False, 'message': _('Missing required fields')})
    
    db = get_db()
    db.execute(
        'INSERT INTO message (user_name, content, created_at) VALUES (?, ?, ?)',
        (user_name, content, datetime.datetime.now())
    )
    db.commit()
    
    return jsonify({'success': True, 'message': _('Message added successfully')})

@app.route('/api/add_message', methods=['POST'])
@login_required
def add_message():
    data = request.json
    user_name = data.get('user_name')
    content = data.get('content')
    
    if not user_name or not content:
        return jsonify({'success': False, 'message': _('Missing required fields')})
    
    db = get_db()
    db.execute(
        'INSERT INTO message (user_name, content, created_at) VALUES (?, ?, ?)',
        (user_name, content, datetime.datetime.now())
    )
    db.commit()
    
    return jsonify({'success': True, 'message': _('Message added successfully')})

@app.route('/api/reply_message', methods=['POST'])
@login_required
def reply_message():
    data = request.json
    message_id = data.get('message_id')
    reply = data.get('reply')
    
    if not message_id or not reply:
        return jsonify({'success': False, 'message': _('Missing required fields')})
    
    db = get_db()
    db.execute(
        'UPDATE message SET reply = ? WHERE id = ?',
        (reply, message_id)
    )
    db.commit()
    
    return jsonify({'success': True, 'message': _('Reply added successfully')})

@app.route('/api/update_photo_description', methods=['POST'])
@login_required
def update_photo_description():
    data = request.json
    photo_id = data.get('photo_id')
    description = data.get('description')
    
    if not photo_id or not description:
        return jsonify({'success': False, 'message': _('Missing required fields')})
    
    db = get_db()
    db.execute(
        'UPDATE photo SET description = ? WHERE id = ?',
        (description, photo_id)
    )
    db.commit()
    
    return jsonify({'success': True, 'message': _('Description updated successfully')})

@app.route('/api/delete_photo', methods=['POST'])
@login_required
def delete_photo():
    data = request.json
    photo_id = data.get('photo_id')
    
    if not photo_id:
        return jsonify({'success': False, 'message': _('Missing photo ID')})
    
    db = get_db()
    
    # Get the filename before deleting the record
    photo = db.execute('SELECT filename FROM photo WHERE id = ?', (photo_id,)).fetchone()
    if not photo:
        return jsonify({'success': False, 'message': _('Photo not found')})
    
    # Delete the record from the database
    db.execute('DELETE FROM photo WHERE id = ?', (photo_id,))
    db.commit()
    
    # Delete the file from the filesystem
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], photo['filename'])
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        # Log the error but don't fail the request
        print(f"Error deleting file: {e}")
    
    # Create response with strong cache control headers
    response = jsonify({'success': True, 'message': _('Photo deleted successfully')})
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/api/update_video_description', methods=['POST'])
@login_required
def update_video_description():
    data = request.json
    video_id = data.get('video_id')
    description = data.get('description')
    
    if not video_id or not description:
        return jsonify({'success': False, 'message': _('Missing required fields')})
    
    db = get_db()
    db.execute(
        'UPDATE video SET description = ? WHERE id = ?',
        (description, video_id)
    )
    db.commit()
    
    return jsonify({'success': True, 'message': _('Description updated successfully')})

@app.route('/api/delete_video', methods=['POST'])
@login_required
def delete_video():
    data = request.json
    video_id = data.get('video_id')
    
    if not video_id:
        return jsonify({'success': False, 'message': _('Missing video ID')})
    
    db = get_db()
    
    # Check if video exists
    video = db.execute('SELECT id FROM video WHERE id = ?', (video_id,)).fetchone()
    if not video:
        return jsonify({'success': False, 'message': _('Video not found')})
    
    # Delete the record from the database
    db.execute('DELETE FROM video WHERE id = ?', (video_id,))
    db.commit()
    
    return jsonify({'success': True, 'message': _('Video deleted successfully')})

@app.route('/api/growth_stories')
def get_growth_stories():
    db = get_db()
    stories = db.execute('SELECT id, entry_date, content FROM growth_story').fetchall()
    
    events = []
    for story in stories:
        events.append({
            'id': story['id'],
            'title': _('Growth Story'),
            'start': story['entry_date'],
            'allDay': True
        })
    
    response = jsonify(events)
    
    # Add cache control headers
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/api/search_growth_stories')
def search_growth_stories():
    query = request.args.get('q', '')
    if not query or len(query) < 2:
        return jsonify({'success': False, 'message': _('Search query too short')})
    
    db = get_db()
    # 使用LIKE进行模糊搜索
    search_param = f'%{query}%'
    stories = db.execute('SELECT id, entry_date, content, image FROM growth_story WHERE content LIKE ?', 
                        (search_param,)).fetchall()
    
    result = []
    for story in stories:
        result.append({
            'id': story['id'],
            'entry_date': story['entry_date'],
            'content': story['content'],
            'image': story['image']
        })
    
    response = jsonify({'success': True, 'stories': result})
    
    # Add cache control headers
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/api/growth_story')
def get_growth_story():
    date = request.args.get('date')
    if not date:
        return jsonify({'success': False, 'message': _('Missing date parameter')})
    
    db = get_db()
    story = db.execute('SELECT * FROM growth_story WHERE entry_date = ?', (date,)).fetchone()
    
    if not story:
        return jsonify({'success': False, 'message': _('No story found for this date')})
    
    response = jsonify({
        'success': True,
        'story': {
            'id': story['id'],
            'entry_date': story['entry_date'],
            'content': story['content'],
            'image': story['image']
        }
    })
    
    # Add cache control headers
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/api/delete_growth_story', methods=['POST'])
@login_required
def delete_growth_story():
    data = request.json
    entry_date = data.get('entry_date')
    
    if not entry_date:
        return jsonify({'success': False, 'message': _('Missing entry date')})
    
    db = get_db()
    
    # Check if story exists
    story = db.execute('SELECT id FROM growth_story WHERE entry_date = ?', (entry_date,)).fetchone()
    if not story:
        return jsonify({'success': False, 'message': _('Story not found')})
    
    # Delete the record from the database
    db.execute('DELETE FROM growth_story WHERE entry_date = ?', (entry_date,))
    db.commit()
    
    return jsonify({'success': True, 'message': _('Story deleted successfully')})

# Direct route to serve uploaded files with no-cache headers
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # 确保上传文件夹存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 打印文件路径以便调试
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(f"Serving file: {file_path}, exists: {os.path.exists(file_path)}")
    
    response = make_response(send_from_directory(app.config['UPLOAD_FOLDER'], filename))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)