from flask_login import UserMixin
from flask import current_app
import json

class User(UserMixin):
    def __init__(self, id_, name, email):
        self.id = id_
        self.name = name
        self.email = email

    @staticmethod
    def get(user_id):
        try:
            redis_client = current_app.config['SESSION_REDIS']
            user_data = redis_client.get(f"user:{user_id}")
            if not user_data:
                return None
            
            user_dict = json.loads(user_data.decode('utf-8'))
            return User(
                id_=user_dict['id_'], 
                name=user_dict['name'], 
                email=user_dict['email'], 
            )
        except Exception as e:
            print(f"Error getting user from Redis: {e}")
            return None

    @staticmethod
    def create(id_, name, email, profile_pic):
        try:
            redis_client = current_app.config['SESSION_REDIS']
            user_data = {
                'id_': id_,
                'name': name,
                'email': email,
                'profile_pic': profile_pic
            }
            # Store user data in Redis with key "user:{id}"
            redis_client.set(f"user:{id_}", json.dumps(user_data))
            return True
        except Exception as e:
            print(f"Error creating user in Redis: {e}")
            return False

    @staticmethod
    def exists(user_id):
        try:
            redis_client = current_app.config['SESSION_REDIS']
            return redis_client.exists(f"user:{user_id}") > 0
        except Exception as e:
            print(f"Error checking user existence in Redis: {e}")
            return False