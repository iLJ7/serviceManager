import sqlite3

class truckDB:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS trucks (reg TEXT PRIMARY KEY, make text, model text, color text, driver text)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM trucks")
        rows = self.cur.fetchall()
        return rows
    
    def insert(self, reg, make, model, color, driver):
        self.cur.execute("INSERT INTO trucks VALUES (?, ?, ?, ?, ?)", (reg, make, model, color, driver))
        self.conn.commit()
    
    def remove(self, reg):
        self.cur.execute("DELETE FROM trucks WHERE reg = ?", (reg,))
        self.conn.commit()
    
    def update(self, reg, driver):
        self.cur.execute("UPDATE trucks SET driver = ? WHERE reg = ?", (driver, reg))
        self.conn.commit()

global truckdb
truckdb = truckDB('trucks.db')
