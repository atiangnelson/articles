from lib.db.database import get_connection


class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name  
        self.category = category  

