-- Initialize the database schema

-- Page content table
CREATE TABLE IF NOT EXISTS page_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_name TEXT UNIQUE,
    content TEXT,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Growth stories table
CREATE TABLE IF NOT EXISTS growth_story (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_date DATE UNIQUE,
    content TEXT,
    image TEXT
);

-- Photos table
CREATE TABLE IF NOT EXISTS photo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    description TEXT,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Videos table
CREATE TABLE IF NOT EXISTS video (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    embed_url TEXT,
    description TEXT,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Messages table
CREATE TABLE IF NOT EXISTS message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT,
    content TEXT,
    reply TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Insert some initial content
INSERT OR IGNORE INTO page_content (page_name, content) VALUES ('index', 'Welcome to Cayden''s Growth Blog!');