from lib.db.database import get_connection


class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name  
        self.category = category  

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or value == "":
            raise ValueError("Magazine name must be a non-empty string.")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or value == "":
            raise ValueError("Magazine category must be a non-empty string.")
        self._category = value
    

def save(self):
    conn = get_connection()
    cursor = conn.cursor()

    if self.id is None:
        cursor.execute(
            "INSERT INTO magazines (name, category) VALUES (?, ?)",
            (self.name, self.category)
        )
        self.id = cursor.lastrowid
    else:
        cursor.execute(
            "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
            (self.name, self.category, self.id)
        )
    conn.commit()
    conn.close()