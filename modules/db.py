
import sqlite3
import datetime
from pathlib import Path

DB_FILE = "chat.db"

def init_db():
    """Initialize the database with necessary tables."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            original_text TEXT,
            translated_text TEXT,
            audio_path TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_message(role, original_text, translated_text, audio_path=None):
    """Save a new message to the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO messages (role, original_text, translated_text, audio_path)
        VALUES (?, ?, ?, ?)
    ''', (role, original_text, translated_text, audio_path))
    conn.commit()
    conn.close()

def get_history():
    """Retrieve all messages ordered by timestamp."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT role, original_text, translated_text, audio_path, timestamp FROM messages ORDER BY timestamp ASC')
    rows = c.fetchall()
    conn.close()
    return rows

def search_messages(query):
    """Search for messages containing the query string."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    search_query = f"%{query}%"
    c.execute('''
        SELECT role, original_text, translated_text, audio_path, timestamp 
        FROM messages 
        WHERE original_text LIKE ? OR translated_text LIKE ?
        ORDER BY timestamp ASC
    ''', (search_query, search_query))
    rows = c.fetchall()
    conn.close()
    return rows

def clear_history():
    """Clear all messages from the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM messages')
    conn.commit()
    conn.close()
