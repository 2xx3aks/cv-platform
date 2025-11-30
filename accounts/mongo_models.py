"""
MongoDB User model using mongoengine as alternative.
This is used if djongo doesn't work well.
"""
from mongoengine import Document, StringField, BooleanField, DateTimeField, ListField
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime


class MongoUser(Document):
    """MongoDB User model using mongoengine."""
    username = StringField(required=True, unique=True, max_length=150)
    email = StringField(required=True, unique=True)
    password = StringField(required=True, max_length=128)
    
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('company', 'Company'),
        ('admin', 'Admin'),
    ]
    role = StringField(choices=ROLE_CHOICES, default='student', max_length=20)
    
    first_name = StringField(max_length=150, default='')
    last_name = StringField(max_length=150, default='')
    
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
    
    date_joined = DateTimeField(default=datetime.utcnow)
    last_login = DateTimeField(null=True)
    
    meta = {
        'collection': 'users',
        'indexes': ['username', 'email']
    }
    
    def set_password(self, raw_password):
        """Set password hash."""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Check password."""
        return check_password(raw_password, self.password)
    
    def is_student(self):
        return self.role == 'student'
    
    def is_company(self):
        return self.role == 'company'
    
    def is_admin(self):
        return self.role == 'admin'
    
    def __str__(self):
        return f"{self.username} ({self.role})"

