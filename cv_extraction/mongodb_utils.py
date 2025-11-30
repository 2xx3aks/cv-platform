"""
MongoDB connection and utility functions.
"""
import pymongo
from pymongo import MongoClient
from django.conf import settings
from typing import Optional, Dict, List
from datetime import datetime


class MongoDBManager:
    """Singleton MongoDB connection manager."""
    _client: Optional[MongoClient] = None
    _db = None
    
    @classmethod
    def get_client(cls):
        """Get MongoDB client instance."""
        if cls._client is None:
            cls._client = MongoClient(settings.MONGODB_URI)
        return cls._client
    
    @classmethod
    def get_database(cls):
        """Get MongoDB database instance."""
        if cls._db is None:
            client = cls.get_client()
            cls._db = client[settings.MONGODB_DB_NAME]
        return cls._db
    
    @classmethod
    def get_cv_collection(cls):
        """Get CV collection."""
        db = cls.get_database()
        return db['cv_profiles']
    
    @classmethod
    def close_connection(cls):
        """Close MongoDB connection."""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None


def save_cv_profile(user_id: int, cv_data: Dict) -> str:
    """
    Save CV profile to MongoDB.
    
    Args:
        user_id: Django User ID
        cv_data: Dictionary containing CV data matching CVExtract schema
    
    Returns:
        MongoDB document ID as string
    """
    collection = MongoDBManager.get_cv_collection()
    
    document = {
        'user_id': user_id,
        'full_name': cv_data.get('full_name', ''),
        'email': cv_data.get('email', ''),
        'phone': cv_data.get('phone', ''),
        'summary': cv_data.get('summary', ''),
        'skills': cv_data.get('skills', []),
        'education': cv_data.get('education', []),
        'experience': cv_data.get('experience', []),
        'certifications': cv_data.get('certifications', []),
        'languages': cv_data.get('languages', []),
        'gpa': cv_data.get('gpa'),
        'major': cv_data.get('major', ''),
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow(),
    }
    
    # Check if profile already exists for this user
    existing = collection.find_one({'user_id': user_id})
    if existing:
        document['updated_at'] = datetime.utcnow()
        collection.update_one(
            {'user_id': user_id},
            {'$set': document}
        )
        return str(existing['_id'])
    else:
        result = collection.insert_one(document)
        return str(result.inserted_id)


def get_cv_profile(user_id: int) -> Optional[Dict]:
    """Get CV profile for a user."""
    collection = MongoDBManager.get_cv_collection()
    profile = collection.find_one({'user_id': user_id})
    if profile:
        profile['_id'] = str(profile['_id'])
    return profile


def get_all_cv_profiles() -> List[Dict]:
    """Get all CV profiles."""
    collection = MongoDBManager.get_cv_collection()
    profiles = list(collection.find())
    for profile in profiles:
        profile['_id'] = str(profile['_id'])
    return profiles


def search_cv_profiles(query: Dict) -> List[Dict]:
    """
    Search CV profiles with filters.
    
    Args:
        query: MongoDB query dictionary
    
    Returns:
        List of matching profiles
    """
    collection = MongoDBManager.get_cv_collection()
    profiles = list(collection.find(query))
    for profile in profiles:
        profile['_id'] = str(profile['_id'])
    return profiles


def delete_cv_profile(user_id: int) -> bool:
    """Delete CV profile for a user."""
    collection = MongoDBManager.get_cv_collection()
    result = collection.delete_one({'user_id': user_id})
    return result.deleted_count > 0


def delete_cv_profile_by_id(profile_id: str) -> bool:
    """Delete CV profile by MongoDB ID."""
    from bson import ObjectId
    collection = MongoDBManager.get_cv_collection()
    try:
        result = collection.delete_one({'_id': ObjectId(profile_id)})
        return result.deleted_count > 0
    except Exception:
        return False

