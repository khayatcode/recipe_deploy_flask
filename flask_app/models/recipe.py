from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the user table from our database
from flask import flash

from flask_app.models.user import User

class Recipe:
    DB = "recipes"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        
    @classmethod
    def save(cls, data):
        query = """ INSERT INTO recipes ( user_id, name, description, instruction, date_made, under_30, created_at, updated_at ) 
        VALUES ( %(user_id)s, %(name)s, %(description)s, %(instruction)s,%(date_made)s, %(under_30)s, NOW() , NOW() ); """
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @classmethod
    def update(cls, data ):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instruction = %(instruction)s, date_made = %(date_made)s, under_30 = %(under_30)s,  updated_at = NOW() WHERE id = %(id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @classmethod
    def get_one(cls, data ):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        result = connectToMySQL(cls.DB).query_db( query, data )
        return cls(result[0])
    
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @staticmethod
    def validate_recipe_data( data ):
        is_valid = True
        if len(data['name']) < 2:
            flash("Name Cannot be less than 2 characters", "recipe")
            is_valid = False
        if len(data['description']) < 3:
            flash("Description cannot be less than 3 charcters", "recipe")
            is_valid = False
        if len(data['description']) > 50:
            flash("Description cannot be more than 50 charcters", "recipe")
            is_valid = False
        if len(data['instruction']) < 3:
            flash("Instruction cannot be less than 3 charcters", "recipe")
            is_valid = False
        if len(data['instruction']) > 50:
            flash("Instruction cannot be more than 50 charcters", "recipe")
            is_valid = False
        if len(data['date_made']) == 0:
            flash("Date cannot be blank", "recipe")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_all_recipes_with_creator(cls):
        # Get all tweets, and their one associated User that created it
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL(cls.DB).query_db(query)
        print(results)
        all_recipes = []
        for row in results:
            
            recipe_data = {
                "id": row['id'], 
                "user_id": row['user_id'],
                "name": row['name'],
                "description": row['description'],
                "instruction": row['instruction'],
                "date_made": row['date_made'],
                "under_30": row['under_30'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }
            
            user_data = {
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            
            one_recipe = cls(recipe_data)
            one_recipe.creator = User(user_data)
            all_recipes.append(one_recipe)
        return all_recipes
