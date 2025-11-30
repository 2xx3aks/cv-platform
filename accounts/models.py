"""
Custom User model with role field.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model with role field.
    Roles: student, company, admin
    """
    ROLE_CHOICES = [
        ('student', _('Student')),
        ('company', _('Company')),
        ('admin', _('Admin')),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student',
        help_text='User role: student, company, or admin'
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} ({self.role})"
    
    def is_student(self):
        return self.role == 'student'
    
    def is_company(self):
        return self.role == 'company'
    
    def is_admin(self):
        return self.role == 'admin'

