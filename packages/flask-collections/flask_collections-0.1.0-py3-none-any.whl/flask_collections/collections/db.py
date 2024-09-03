from .files import DataFileCollection
import sqlite3


class SQLiteCollection(DataFileCollection):
    file_exts = ("db", "sqlite", "sqlite3")
    
    def __init__(self, app, name, path, query, **kwargs):
        super().__init__(app, name, path, **kwargs)
        self.query = query
    
    def _iter_entries(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        for row in c.execute(self.query):
            yield self.entry_cls.from_data(self, row)
        c.close()
        conn.close()