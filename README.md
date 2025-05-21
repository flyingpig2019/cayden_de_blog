# Cayden's Growth Blog

A personal blog application built with Flask to document Cayden's growth journey. This application includes photo galleries, video collections, growth stories with calendar integration, and a message board for visitors.

## Features

- **Multilingual Support**: Toggle between English and Chinese
- **Photo Gallery**: Upload and manage photos
- **Video Collection**: Embed and manage videos
- **Growth Stories**: Calendar-based growth journey documentation
- **Message Board**: Allow visitors to leave messages with admin replies
- **Admin Dashboard**: Secure admin area for content management
- **Inline Editing**: Edit content directly on the page when logged in as admin

## Project Structure

```
/cayden_blog/
│
├── app.py                 # Main Flask application
├── schema.sql             # Database schema
├── requirements.txt       # Dependencies
├── .env                   # Environment variables
├── babel.cfg              # Babel configuration for translations
│
├── templates/             # HTML templates
│   ├── base.html          # Base template with header, footer, etc.
│   ├── index.html         # Home page
│   ├── photos.html        # Photo gallery
│   ├── videos.html        # Video collection
│   ├── growth.html        # Growth stories with calendar
│   ├── messages.html      # Message board
│   ├── admin.html         # Admin dashboard
│   └── login.html         # Admin login
│
├── static/
│   ├── css/
│   │   └── style.css      # Main stylesheet
│   ├── js/
│   │   ├── main.js        # Main JavaScript file
│   │   └── admin.js       # Admin-specific JavaScript
│   └── uploads/           # Uploaded images
│
└── translations/          # Language translations (generated)
```

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Clone the repository or download the source code

2. Navigate to the project directory

3. Create a virtual environment (recommended):
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

6. Initialize the database:
   ```
   flask init-db
   ```

7. Run the application:
   ```
   flask run
   ```

8. Access the application in your browser at `http://127.0.0.1:5000`

### Admin Access

Use the following credentials to log in as admin:
- Email: The email specified in your .env file (default: grand.cayden@gmail.com)
- Authentication Code: Optional TOTP code if configured

## Translation Management

To extract messages for translation:

```
pybabel extract -F babel.cfg -o messages.pot .
pybabel init -i messages.pot -d translations -l zh
```

Edit the translation files in `translations/zh/LC_MESSAGES/messages.po`

Compile translations:

```
pybabel compile -d translations
```

## License

This project is for personal use only.

## Support

For any issues or questions, please contact the administrator.