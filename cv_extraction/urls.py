"""
URL configuration for CV extraction app.
"""
from django.urls import path
from . import views

app_name = 'cv_extraction'

urlpatterns = [
    path('', views.home, name='home'),
    
    # Student routes
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/upload/', views.upload_cv, name='upload_cv'),
    path('student/extracted-data/', views.show_extracted_data, name='show_extracted_data'),
    path('student/browse/', views.student_browse, name='student_browse'),
    path('student/profile/', views.student_profile, name='student_profile'),
    path('student/profile/<int:user_id>/', views.student_profile, name='student_profile_view'),
    path('student/edit-cv/', views.edit_cv_profile, name='edit_cv_profile'),
    
    # Company routes
    path('company/dashboard/', views.company_dashboard, name='company_dashboard'),
    path('company/compare/', views.compare_students, name='compare_students'),
    
    # Admin routes (using 'manage' prefix to avoid conflict with Django admin)
    path('manage/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage/users/', views.admin_users, name='admin_users'),
    path('manage/users/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
    path('manage/users/<int:user_id>/edit/', views.admin_edit_user, name='admin_edit_user'),
    path('manage/users/<int:user_id>/edit-cv/', views.admin_edit_cv_profile, name='admin_edit_cv_profile'),
    path('manage/delete-user/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),
    path('manage/delete-cv/<int:user_id>/', views.admin_delete_cv, name='admin_delete_cv'),
]

