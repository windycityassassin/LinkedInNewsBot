import sqlite3
from dataclasses import asdict

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS news_articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                url TEXT UNIQUE,
                source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def store_news(self, articles):
        for article in articles:
            try:
                self.cursor.execute('''
                    INSERT INTO news_articles (title, url, source)
                    VALUES (:title, :url, :source)
                ''', asdict(article))
            except sqlite3.IntegrityError:
                # Article already exists, skip
                pass
        self.conn.commit()

    def get_recent_news(self, limit=10):
        self.cursor.execute('''
            SELECT title, url, source FROM news_articles
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()