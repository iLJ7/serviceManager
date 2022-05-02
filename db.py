import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS services (id INTEGER PRIMARY KEY, serviceType text, cost text)")
        self.conn.commit()
    
    def fetch(self):
        self.cur.execute("SELECT * FROM services")
        rows = self.cur.fetchall()
        return rows
    
    def insert(self, serviceType, cost):
        self.cur.execute("INSERT INTO services VALUES (NULL, ?, ?)", (serviceType, cost))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM services WHERE id=?", (id,))
        self.conn.commit()
    
    def update(self, id, serviceType, cost):
        self.cur.execute("UPDATE services SET serviceType = ?, cost = ? WHERE id = ?", (serviceType, cost, id))
        self.conn.commit()
    
    def __del__(self):
        self.conn.close()
