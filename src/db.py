from pathlib import Path
import sqlite3
from datetime import datetime


class DatabaseConnection:

    con: sqlite3.Connection
    cur: sqlite3.Cursor

    def __init__(self, path_to_db: Path) -> None:
        self.con = sqlite3.connect(str(path_to_db))
        self.cur = self.con.cursor()   

    def close(self) -> None:
        self.con.close()


class Database:

    PATH_TO_DB: Path = Path.home() / '.tnt' / 'db.sqlite3'
    db_connection: DatabaseConnection

    def __init__(self) -> None:
        self.db_connection = DatabaseConnection(path_to_db=self.PATH_TO_DB)

    def create(self) -> None:
        self.db_connection.cur.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        ''')

        self.db_connection.cur.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                datetime TEXT
            )
        ''')

        self.db_connection.cur.execute('''
            CREATE TABLE IF NOT EXISTS notes_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag INTEGER REFERENCES tags (id),
                note INTEGER REFERENCES notes (id)
            )
        ''')

        self.db_connection.con.commit()

    def create_note(self, text: str) -> int:
        now = datetime.now()
        params = (None, text, now.isoformat(timespec='seconds'))

        res = self.db_connection.cur.execute('INSERT INTO notes VALUES(?, ?, ?) RETURNING id', params)
        result = res.fetchone()

        self.db_connection.con.commit()
        return result[0]
    
    def get_tag(self, name: str) -> int | None:
        params = (name,)
        
        res = self.db_connection.cur.execute('SELECT id FROM tags WHERE name = ?', params)
        result = res.fetchone()

        if result is None:
            return None

        return result[0]

    def create_tag(self, name: str) -> int:
        params = (None, name)
        
        res = self.db_connection.cur.execute('INSERT INTO tags VALUES(?, ?) RETURNING id', params)
        result = res.fetchone()

        self.db_connection.con.commit()
        return result[0]


database = Database()
