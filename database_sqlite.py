import sqlite3

class DatabaseSQLITE:
    def __init__(self, db_name):
        self.conn = sqlite3.connect("data/databases/"+db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        try:
            columns_str = ', '.join(columns)
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})")
            self.conn.commit()
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))

    def insert_data(self, table_name, value_names, data):
        try:
            placeholders = ', '.join(['?'] * len(data))
            value_names =', '.join(value_names)
            self.cursor.execute(f"INSERT INTO {table_name} ({value_names}) VALUES ({placeholders})", data)
            self.conn.commit()
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))

    def fetch_data(self, table_name, condition=None):
        try:
            if condition:
                self.cursor.execute(f"SELECT * FROM {table_name} WHERE {condition}")
            else:
                self.cursor.execute(f"SELECT * FROM {table_name}")
            return self.cursor.fetchall()
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))

    def close(self):
        self.cursor.close()
        self.conn.close()
