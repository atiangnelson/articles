from lib.db.connection import get_connection

class Author:
    def __init__(self,name,id=None):
        self.id=id
        self.name=name

    
    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self.id = cursor.lastrowid
        else:
            cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))

        conn.commit()
        conn.close()
    