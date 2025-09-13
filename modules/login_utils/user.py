from flask_login import UserMixin
from flask import current_app
import json
import logging
from datetime import timedelta
logger = logging.getLogger(__name__)

class User(UserMixin):
    def __init__(self, id_, name, email):
        self.id = id_
        self.name = name
        self.email = email

    @staticmethod
    def _get_redis_client():
        """Get Redis client with error handling"""
        try:
            return current_app.config['SESSION_REDIS']
        except Exception as e:
            logger.error(f"Redis connection error: {e}")
            return None

    @staticmethod
    def get(user_id):
        """Get user from Redis with improved error handling and validation"""
        if not user_id:
            return None
            
        redis_client = User._get_redis_client()
        if not redis_client:
            return None
            
        try:
            user_data = redis_client.get(f"user:{user_id}")
            if not user_data:
                return None
            
            user_dict = json.loads(user_data.decode('utf-8'))
            
            # Validate required fields
            required_fields = ['id_', 'name', 'email']
            if not all(field in user_dict for field in required_fields):
                logger.error(f"Invalid user data structure for user {user_id}")
                return None
                
            return User(
                id_=user_dict['id_'], 
                name=user_dict['name'], 
                email=user_dict['email']
            )
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error for user {user_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting user {user_id} from Redis: {e}")
            return None

    @staticmethod
    def create(id_, name, email):
        """Create user in Redis with validation and error handling"""
        if not all([id_, name, email]):
            logger.error("Missing required user data for creation")
            return False
            
        # Basic email validation
        if '@' not in email or '.' not in email:
            logger.error(f"Invalid email format: {email}")
            return False
            
        redis_client = User._get_redis_client()
        if not redis_client:
            return False
            
        try:
            user_data = {
                'id_': str(id_),
                'name': str(name),
                'email': str(email)
            }
            
            # Set user data with expiration (optional: 30 days)
            key = f"user:{id_}"
            success = redis_client.setex(
                key, 
                timedelta(days=30), 
                json.dumps(user_data)
            )
            
            if success:
                logger.info(f"User {id_} created successfully")
                return True
            else:
                logger.error(f"Failed to create user {id_} in Redis")
                return False
                
        except Exception as e:
            logger.error(f"Error creating user {id_} in Redis: {e}")
            return False

    @staticmethod
    def exists(user_id):
        """Check if user exists with improved error handling"""
        if not user_id:
            return False
            
        redis_client = User._get_redis_client()
        if not redis_client:
            return False
            
        try:
            return redis_client.exists(f"user:{user_id}") > 0
        except Exception as e:
            logger.error(f"Error checking user existence for {user_id}: {e}")
            return False

    @staticmethod
    def delete(user_id):
        """Delete user from Redis"""
        if not user_id:
            return False
            
        redis_client = User._get_redis_client()
        if not redis_client:
            return False
            
        try:
            result = redis_client.delete(f"user:{user_id}")
            if result:
                logger.info(f"User {user_id} deleted successfully")
                return True
            else:
                logger.warning(f"User {user_id} not found for deletion")
                return False
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            return False

    def update(self, name=None, email=None):
        """Update user information"""
        redis_client = User._get_redis_client()
        if not redis_client:
            return False
            
        try:
            # Update instance variables
            if name:
                self.name = name
            if email:
                if '@' not in email or '.' not in email:
                    logger.error(f"Invalid email format: {email}")
                    return False
                self.email = email
            
            # Update in Redis
            user_data = {
                'id_': self.id,
                'name': self.name,
                'email': self.email
            }
            
            key = f"user:{self.id}"
            success = redis_client.setex(
                key,
                timedelta(days=30),
                json.dumps(user_data)
            )
            
            if success:
                logger.info(f"User {self.id} updated successfully")
                return True
            else:
                logger.error(f"Failed to update user {self.id}")
                return False
                
        except Exception as e:
            logger.error(f"Error updating user {self.id}: {e}")
            return False

    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }