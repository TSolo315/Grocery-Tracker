import sqlite3


class DatabaseManager:
    def __init__(self, database_file):
        self.conn = sqlite3.connect(database_file)
        self.cursor = self.conn.cursor()

    def save(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
