
import sqlite3
import datetime
from pathlib import Path

DB_FILE = "chat.db"

def conn_db():
    """Create a thread-safe connection with a longer timeout."""
    return sqlite3.connect(DB_FILE, check_same_thread=False, timeout=30)

def init_db():
    """Initialize the database with necessary tables."""
    conn = conn_db()
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
    conn = conn_db()
    try:
        c = conn.cursor()
        c.execute('''
            INSERT INTO messages (role, original_text, translated_text, audio_path)
            VALUES (?, ?, ?, ?)
        ''', (role, original_text, translated_text, audio_path))
        conn.commit()
    finally:
        conn.close()

def get_history():
    """Retrieve all messages ordered by timestamp."""
    conn = conn_db()
    try:
        c = conn.cursor()
        c.execute('SELECT role, original_text, translated_text, audio_path, timestamp FROM messages ORDER BY timestamp ASC')
        rows = c.fetchall()
        return rows
    finally:
        conn.close()

def search_messages(query):
    """Search for messages containing the query string."""
    conn = conn_db()
    try:
        c = conn.cursor()
        search_query = f"%{query}%"
        c.execute('''
            SELECT role, original_text, translated_text, audio_path, timestamp 
            FROM messages 
            WHERE original_text LIKE ? OR translated_text LIKE ?
            ORDER BY timestamp ASC
        ''', (search_query, search_query))
        rows = c.fetchall()
        return rows
    finally:
        conn.close()

def clear_history():
    """Clear all messages from the database."""
    conn = conn_db()
    try:
        c = conn.cursor()
        c.execute('DELETE FROM messages')
        conn.commit()
    finally:
        conn.close()
