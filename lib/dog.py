import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None  # Will be assigned when saved to the database

    @classmethod
    def create_table(cls):
        CURSOR.execute("CREATE TABLE IF NOT EXISTS dogs (id INTEGER PRIMARY KEY, name TEXT, breed TEXT)")
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS dogs")
        CONN.commit()

    def save(self):
        if self.id is None:
            # Insert a new row into the database
            CURSOR.execute("INSERT INTO dogs (name, breed) VALUES (?, ?)", (self.name, self.breed))
            self.id = CURSOR.lastrowid
        else:
            # Update an existing row in the database
            CURSOR.execute("UPDATE dogs SET name=?, breed=? WHERE id=?", (self.name, self.breed, self.id))
        CONN.commit()

    @classmethod
    def create(cls, name, breed):
        new_dog = cls(name, breed)
        new_dog.save()
        return new_dog

    @classmethod
    def new_from_db(cls, row):
        id, name, breed = row
        dog = cls(name, breed)
        dog.id = id
        return dog

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM dogs")
        rows = CURSOR.fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        CURSOR.execute("SELECT * FROM dogs WHERE name=?", (name,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute("SELECT * FROM dogs WHERE id=?", (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None
