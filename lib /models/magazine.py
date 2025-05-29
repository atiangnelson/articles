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

    @classmethod
    def find_by_id(cls, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (magazine_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row["name"], row["category"], row["id"])
        return None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row["name"], row["category"], row["id"])
        return None

    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(row["name"], row["category"], row["id"]) for row in rows]

    def articles(self):
        from lib.models.article import Article
        return Article.find_by_magazine(self.id)

    def authors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT authors.id, authors.name
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()

        from lib.models.author import Author

        return [Author(row["name"], row["id"]) for row in rows]
    

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT title FROM articles WHERE magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [row["title"] for row in rows]

    def contributing_authors(self):
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT authors.id, authors.name, COUNT(articles.id) as article_count
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(row["name"], row["id"]) for row in rows]


    @classmethod
    def with_multiple_authors(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT magazines.id, magazines.name, magazines.category
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            GROUP BY magazines.id
            HAVING COUNT(DISTINCT articles.author_id) >= 2
        """)
        rows = cursor.fetchall()
        conn.close()

        return [cls(row["name"], row["category"], row["id"]) for row in rows]

    @classmethod
    def article_counts(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT magazines.id, magazines.name, magazines.category, COUNT(articles.id) AS article_count
            FROM magazines
            LEFT JOIN articles ON magazines.id = articles.magazine_id
            GROUP BY magazines.id
        """)
        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "id": row["id"],
                "name": row["name"],
                "category": row["category"],
                "article_count": row["article_count"],
            }
            for row in rows
        ]