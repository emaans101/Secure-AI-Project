"""
Database and alerts management for the Learnova AI platform.
Handles SQLite database initialization and alert CRUD operations.
"""

import sqlite3
from flask import jsonify

DATABASE = 'alerts.db'


def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with alerts table"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            alert_type TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            resolved INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()


def get_all_alerts():
    """Fetch all unresolved alerts from database"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            SELECT id, student_name, alert_type, message, timestamp, resolved
            FROM alerts
            WHERE resolved = 0
            ORDER BY timestamp DESC
        ''')
        alerts = c.fetchall()
        conn.close()
        
        # Convert to list of dicts
        result = []
        for row in alerts:
            result.append({
                'id': row['id'],
                'student_name': row['student_name'],
                'alert_type': row['alert_type'],
                'message': row['message'],
                'timestamp': row['timestamp'],
                'resolved': row['resolved']
            })
        
        return result
    except Exception as e:
        raise Exception(f"Error fetching alerts: {str(e)}")


def create_alert(student_name, alert_type, message):
    """Create a new alert in the database"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO alerts (student_name, alert_type, message)
            VALUES (?, ?, ?)
        ''', (student_name, alert_type, message))
        conn.commit()
        alert_id = c.lastrowid
        conn.close()
        
        return alert_id
    except Exception as e:
        raise Exception(f"Error creating alert: {str(e)}")


def seed_sample_alerts():
    """Seed the database with sample alerts (for development/testing)"""
    try:
        sample_alerts = [
            ("Jordan M.", "Chatbot safety", "Attempted to bypass chatbot rules with repeated prompt-injection style text."),
            ("Mia R.", "Needs attention", "Has asked for help 4 times in 20 minutes and appears stuck on algebra assignment 3."),
            ("Leo K.", "Chatbot safety", "Requested direct final answers repeatedly without showing work attempt."),
            ("Sofia T.", "Needs attention", "Gave very low-energy responses to the AI and described feeling extremely sad; this may indicate a mental health concern."),
        ]
        
        conn = get_db()
        c = conn.cursor()
        
        for student_name, alert_type, message in sample_alerts:
            c.execute('''
                INSERT INTO alerts (student_name, alert_type, message)
                VALUES (?, ?, ?)
            ''', (student_name, alert_type, message))
        
        conn.commit()
        conn.close()
        
        return len(sample_alerts)
    except Exception as e:
        raise Exception(f"Error seeding alerts: {str(e)}")
