import sqlite3

database = sqlite3.connect("kokkilokki.db")

class User:
    def __init__(self, username: str, password: str):
        self.__username = username
        self.__password = password
        database.execute("""INSERT INTO Users (username, password_hash) 
                         VALUES (?, ?)""", [username, password])
        self.__id = database.execute("""SELECT id 
                                     FROM Users 
                                     WHERE username = ?""", [username])

    def __password_hash(password: str):
        pass

    def add_recipe(self, name: str):
        database.execute("""INSERT INTO Recipes (title, user) 
                         VALUES (?, ?)""", [name, self.__id])

    def delete_recipe(self, recipe_id: int):
        database.execute("""DELETE FROM Recipes id = ?""", [recipe_id])

    def change_recipe(self):
        pass

    def search_recipes(self, username: str):
        if username == "":
            recipes = database.execute("""SELECT id, title 
                                       FROM Recipes 
                                       ORDER BY id""").fetchall()
        else:
            recipes = database.execute("""SELECT r.id, r.title
                                       FROM Recipes r, Users u 
                                       WHERE u.name = ? AND r.user_id = u.id 
                                       ORDER BY r.id""", [username]).fetchall()
        return recipes
    
    def add_comment(self):
        pass

    def add_review(self):
        pass


class recipe:
    def __init__(self):
        self.__ingredients = []
        self.__equipment = []

    def add_ingredient(self, ingredient: str, amount: int):
        added = (ingredient, amount)
        self.__ingredients.append(added)
        return added
    
    def add_equipment(self, equipment: str, size: int):
        added = (equipment, size)
        self.__equipment.append(added)
        return added
    
    def add_step(self, step: str):
        pass

    def imperial(self):
        pass