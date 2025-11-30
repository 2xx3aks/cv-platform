# User Management Guide

This guide explains how to create and manage different user roles (Admin, Company, and Student) in the CV Platform.

## Table of Contents
1. [Creating Users](#creating-users)
2. [Admin Account](#admin-account)
3. [Company Account](#company-account)
4. [Student Account](#student-account)
5. [Managing Users](#managing-users)
6. [Quick Start](#quick-start)

---

## Creating Users

### Method 1: Registration Page (Public)

1. Navigate to: `http://127.0.0.1:8000/accounts/register/`
2. Fill in the registration form:
   - **Username**: Choose a unique username
   - **Email**: Enter your email address
   - **Password**: Create a secure password
   - **Confirm Password**: Re-enter your password
   - **Role**: Select from dropdown:
     - Student
     - Company
     - Admin (if available)
3. Click **Register**
4. You will be automatically logged in and redirected to your dashboard

### Method 2: Django Admin Panel (For Admins)

1. Navigate to: `http://127.0.0.1:8000/admin/`
2. Login with admin credentials
3. Go to **Accounts** → **Users**
4. Click **Add User** (top right)
5. Fill in:
   - **Username**: Required
   - **Password**: Set password
   - **Email**: Optional
   - **Role**: Select from dropdown
6. Click **Save**

### Method 3: Admin Dashboard (For Admins)

1. Login as Admin
2. Navigate to: `http://127.0.0.1:8000/manage/dashboard/`
3. Click **Manage Users** button
4. Click **Add New User** (if available) or use Django Admin

---

## Admin Account

### Creating an Admin Account

#### Option 1: Using Django Shell (Recommended)

```bash
# Activate virtual environment
cd D:\Ai Procurement\front\Procurement-MVP-Engine\src\routers\test
venv\Scripts\activate

# Run Django shell
python cv_platform\manage.py shell
```

Then in the shell:
```python
from accounts.models import User

# Create admin user
admin = User.objects.create_user(
    username='admin',
    email='admin@example.com',
    password='admin123',  # Change this!
    role='admin'
)
admin.is_staff = True
admin.is_superuser = True
admin.save()
print(f"Admin user '{admin.username}' created successfully!")
```

#### Option 2: Using Django Admin (If you have superuser)

1. Go to `http://127.0.0.1:8000/admin/`
2. Login with superuser account
3. Create new user and set role to "Admin"

#### Option 3: Using Management Command

Create a file `create_admin.py`:
```python
import os
import sys
import django

sys.path.insert(0, '.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cv_platform.settings')
django.setup()

from accounts.models import User

admin = User.objects.create_user(
    username='admin',
    email='admin@example.com',
    password='admin123',
    role='admin'
)
admin.is_staff = True
admin.is_superuser = True
admin.save()
print("Admin created!")
```

Run: `python create_admin.py`

### Admin Features

- **Dashboard**: `http://127.0.0.1:8000/manage/dashboard/`
- **View Analytics**: Charts, statistics, user counts
- **Manage Users**: View, edit, delete all users
- **Edit User Info**: Username, email, password, role
- **Edit CV Profiles**: Modify any student's CV data
- **Delete Users**: Remove users and their CV profiles
- **Delete CVs**: Remove CV profiles only

### Admin Login

1. Go to: `http://127.0.0.1:8000/accounts/login/`
2. Enter admin username and password
3. You'll be redirected to Admin Dashboard

---

## Company Account

### Creating a Company Account

#### Option 1: Registration Page

1. Go to: `http://127.0.0.1:8000/accounts/register/`
2. Select **Role: Company**
3. Fill in registration form
4. Click **Register**

#### Option 2: Admin Creates Company

1. Login as Admin
2. Go to: `http://127.0.0.1:8000/manage/users/`
3. Click **Add User** or use Django Admin
4. Set role to **Company**

#### Option 3: Django Shell

```python
from accounts.models import User

company = User.objects.create_user(
    username='company1',
    email='company@example.com',
    password='company123',
    role='company'
)
print(f"Company user '{company.username}' created!")
```

### Company Features

- **Dashboard**: `http://127.0.0.1:8000/company/dashboard/`
- **Browse Students**: View all student profiles
- **Filter Students**: By GPA, major, skills
- **Search**: Full-text search in student profiles
- **Compare Students**: Compare 2-3 students side by side
- **View Profiles**: See detailed CV information

### Company Login

1. Go to: `http://127.0.0.1:8000/accounts/login/`
2. Enter company username and password
3. You'll be redirected to Company Dashboard

---

## Student Account

### Creating a Student Account

#### Option 1: Registration Page (Most Common)

1. Go to: `http://127.0.0.1:8000/accounts/register/`
2. Select **Role: Student** (default)
3. Fill in registration form
4. Click **Register**

#### Option 2: Admin Creates Student

1. Login as Admin
2. Go to: `http://127.0.0.1:8000/manage/users/`
3. Create new user with role **Student**

#### Option 3: Django Shell

```python
from accounts.models import User

student = User.objects.create_user(
    username='student1',
    email='student@example.com',
    password='student123',
    role='student'
)
print(f"Student user '{student.username}' created!")
```

### Student Features

- **Dashboard**: `http://127.0.0.1:8000/student/dashboard/`
- **Upload CV**: Upload PDF or DOCX CV file
- **View Profile**: See extracted CV data
- **Edit Profile**: Update personal information
- **Edit CV Data**: Modify extracted CV information
- **Browse Students**: View other students' public profiles

### Student Login

1. Go to: `http://127.0.0.1:8000/accounts/login/`
2. Enter student username and password
3. You'll be redirected to Student Dashboard

---

## Managing Users

### As an Admin

#### View All Users

1. Login as Admin
2. Go to: `http://127.0.0.1:8000/manage/users/`
3. See list of all users with their roles

#### Edit User

1. Go to: `http://127.0.0.1:8000/manage/users/`
2. Click on a user
3. Click **Edit User** button
4. Modify:
   - Username
   - Email
   - First Name / Last Name
   - Role (Student/Company/Admin)
   - Password (optional)
   - Active Status
5. Click **Save Changes**

#### Edit CV Profile

1. Go to user details page
2. Click **Edit CV Profile** button
3. Modify all CV fields:
   - Personal info (name, email, phone)
   - Education, Experience, Skills
   - Certifications, Languages
   - GPA, Major
4. Click **Save Changes**

#### Delete User

1. Go to user details page
2. Click **Delete User** button
3. Confirm deletion
4. User and CV profile will be permanently deleted

#### Delete CV Only

1. Go to user details page
2. Click **Delete CV** button
3. Confirm deletion
4. Only CV profile is deleted, user account remains

### Using Django Admin Panel

1. Go to: `http://127.0.0.1:8000/admin/`
2. Login with admin credentials
3. Navigate to **Accounts** → **Users**
4. Manage users with full Django admin features

---

## Quick Start

### Create Your First Admin (One-Time Setup)

```bash
# Navigate to project directory
cd D:\Ai Procurement\front\Procurement-MVP-Engine\src\routers\test

# Activate virtual environment
venv\Scripts\activate

# Run Django shell
python cv_platform\manage.py shell
```

```python
from accounts.models import User

# Create admin
admin = User.objects.create_user(
    username='admin',
    email='admin@cvplatform.com',
    password='admin123',  # CHANGE THIS PASSWORD!
    role='admin'
)
admin.is_staff = True
admin.is_superuser = True
admin.save()
print("✅ Admin created! Username: admin, Password: admin123")
```

### Create Test Users

```python
# Create a company
company = User.objects.create_user(
    username='company1',
    email='company@test.com',
    password='company123',
    role='company'
)

# Create a student
student = User.objects.create_user(
    username='student1',
    email='student@test.com',
    password='student123',
    role='student'
)

print("✅ Test users created!")
```

### Login URLs

- **Login Page**: `http://127.0.0.1:8000/accounts/login/`
- **Admin Dashboard**: `http://127.0.0.1:8000/manage/dashboard/`
- **Company Dashboard**: `http://127.0.0.1:8000/company/dashboard/`
- **Student Dashboard**: `http://127.0.0.1:8000/student/dashboard/`

---

## User Roles Summary

| Role | Default Dashboard | Key Features |
|------|------------------|-------------|
| **Admin** | `/manage/dashboard/` | Manage users, view analytics, edit/delete users and CVs |
| **Company** | `/company/dashboard/` | Browse students, filter, search, compare candidates |
| **Student** | `/student/dashboard/` | Upload CV, view/edit profile, browse other students |

---

## Troubleshooting

### Can't Login?

1. Check username and password are correct
2. Verify user account is **Active** (Admin can check this)
3. Clear browser cookies and try again
4. Check if user exists: Use Django shell to verify

### User Not Redirecting Correctly?

- Admin should go to `/manage/dashboard/`
- Company should go to `/company/dashboard/`
- Student should go to `/student/dashboard/`

If wrong redirect, check user's role in database.

### Forgot Admin Password?

Reset using Django shell:
```python
from accounts.models import User

admin = User.objects.get(username='admin')
admin.set_password('newpassword123')
admin.save()
print("Password reset!")
```

---

## Security Notes

⚠️ **Important**:
- Change default passwords immediately
- Use strong passwords in production
- Don't share admin credentials
- Regularly review user accounts
- Deactivate unused accounts instead of deleting

---

## Need Help?

- Check Django admin panel: `/admin/`
- View user details: `/manage/users/<user_id>/`
- Check application logs for errors
- Verify database connection

---

**Last Updated**: 2025
**Version**: 1.0

