from lib.db.connection import get_connection

class Article:
    def __init__(self, title, author_id, magazine_id, id=None):
        self.id = id
        self.title = title  
        self.author_id = author_id
        self.magazine_id = magazine_id