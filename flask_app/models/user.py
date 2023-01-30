from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the user table from our database
from flask import flash
import re

password_regex = re.compile(r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    DB = "recipes"
    def __init__( self , data ):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.id = data['id']
        self.recipes = []
    
    @classmethod
    def get_one(cls, data ):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        result = connectToMySQL(cls.DB).query_db( query, data )
        return cls(result[0])
    
    @classmethod
    def get_by_email(cls, data ):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        # data is a dictionary that will be passed into the save method from server.py
        result = connectToMySQL(cls.DB).query_db( query, data )
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email, password , created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s, %(password)s, NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @staticmethod
    def validate_regist( data ):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        # data is a dictionary that will be passed into the save method from server.py
        result = connectToMySQL('recipes').query_db( query, data )
        if len(data['first_name']) == 0 or len(data['last_name']) == 0 or len(data['email']) == 0 or len(data['password']) == 0 or len(data['confpass']) == 0:
            flash("All field required!", "register" )
            is_valid = False
            return is_valid
        if len(result) >= 1:
            flash("Email already in use!", "register")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email!!!", "register")
            is_valid = False
        if len(data['first_name']) < 3:
            flash("First name must be at least 3 characters", "register")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 characters", "register")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if data['password'] != data['confpass']:
            flash("Passwords don't match", "register")
            is_valid = False
        if not password_regex.match(data['password']):
            flash("Password must contain at least one capital letter and one number", "register")
            is_valid = False
        return is_valid