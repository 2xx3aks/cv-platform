# CV Platform - Complete Documentation & Setup Guide

**Version:** 2.0  
**Last Updated:** November 2025  
**Platform Support:** Windows, macOS, Linux

---

## Table of Contents

1. [Application Overview](#application-overview)
2. [Prerequisites & Requirements](#prerequisites--requirements)
3. [Installation Guide](#installation-guide)
   - [Windows Setup](#windows-setup)
   - [macOS Setup](#macos-setup)
   - [Linux Setup](#linux-setup)
4. [Quick Start](#quick-start)
5. [Features & User Roles](#features--user-roles)
6. [Technology Stack](#technology-stack)
7. [Configuration](#configuration)
8. [Usage Guide](#usage-guide)
9. [API & Data Schema](#api--data-schema)
10. [Troubleshooting](#troubleshooting)
11. [Advanced Topics](#advanced-topics)

---

## Application Overview

### What is CV Platform?

The **CV Platform** is a Django-based web application that automates CV processing and connects companies with talented graduates. It uses artificial intelligence (Cohere API) to extract structured data from resumes and provides role-based dashboards for different users.

### Key Capabilities

- **Automated CV Extraction**: Uses Cohere AI to intelligently parse CV documents
- **Multi-Role System**: Student, Company, and Admin user types
- **Bilingual Interface**: Full support for English and Arabic (العربية)
- **Advanced Filtering**: Companies can search and filter candidates by multiple criteria
- **Comparative Analysis**: Compare 2-3 students side-by-side
- **Analytics Dashboard**: Admin dashboard with comprehensive statistics
- **MongoDB Integration**: Secure, scalable document storage
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

### User Roles

| Role | Purpose | Key Features |
|------|---------|--------------|
| **Student** | Upload and manage CV | Upload CV, view extracted data, browse other students, edit profile |
| **Company** | Find and evaluate candidates | Browse students, filter by criteria, search, compare candidates |
| **Admin** | Manage platform | User management, analytics, delete users/CVs, system oversight |

---

## Prerequisites & Requirements

### System Requirements

#### Minimum Requirements
- **CPU**: Dual-core processor (2+ GHz)
- **RAM**: 4 GB minimum (8 GB recommended)
- **Disk Space**: 2 GB free space
- **Internet**: Required for Cohere API

#### Supported Operating Systems
- ✅ Windows 10/11 (64-bit)
- ✅ macOS 10.14+ (Intel or Apple Silicon)
- ✅ Linux (Ubuntu 18.04+, Debian, etc.)

### Software Requirements

#### Python
- **Python 3.8 or higher** (3.9+ recommended)
- Download: https://www.python.org/downloads/

#### MongoDB
- **MongoDB 4.0 or higher**
- Download: https://www.mongodb.com/try/download/community
- Or use MongoDB Atlas (cloud): https://www.mongodb.com/cloud/atlas

#### Cohere API
- Free API key from: https://cohere.com/
- Sign up and generate API key in your dashboard

#### Git (Optional)
- For cloning the repository
- Download: https://git-scm.com/

---

## Installation Guide

### Windows Setup

#### Step 1: Install Python

1. Download Python 3.9+ from https://www.python.org/downloads/
2. **Important**: Check the box "Add Python to PATH" during installation
3. Open Command Prompt and verify:
   ```cmd
   python --version
   ```
   Should show: `Python 3.9.x` or higher

#### Step 2: Install MongoDB

**Option A: MongoDB Community Edition (Local)**
1. Download from https://www.mongodb.com/try/download/community
2. Run the installer
3. Choose "MongoDB Community Server"
4. Let it install as a service (recommended)
5. Verify installation by opening Command Prompt:
   ```cmd
   mongosh
   ```
   Should open MongoDB shell

**Option B: MongoDB Atlas (Cloud - No Installation)**
1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free account
3. Create a cluster
4. Get your connection string (will use in `.env` file)
5. No local installation needed

#### Step 3: Clone or Download Project

**Option A: Using Git**
```cmd
git clone <repository-url>
cd cv-platform
```

**Option B: Manual Download**
1. Download the project as ZIP
2. Extract to desired location
3. Open Command Prompt in extracted folder

#### Step 4: Create Virtual Environment

```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your command prompt
```

#### Step 5: Install Dependencies

```cmd
# Ensure pip is up to date
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

**Expected output**: Successfully installed [number] packages

#### Step 6: Configure Environment

Create a `.env` file in the project root directory with:

```env
# Cohere API Key (get from https://cohere.com)
COHERE_API_KEY=your-cohere-api-key-here

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB_NAME=cv_platform

# Django Configuration
DJANGO_SECRET_KEY=your-secret-key-here-change-in-production

# Optional: For production
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Important Notes:**
- Never commit `.env` to version control
- Keep your API key confidential
- Change `DJANGO_SECRET_KEY` for production

#### Step 7: Initialize Database

```cmd
# Navigate to cv_platform directory
cd cv_platform

# Create database tables
python manage.py migrate --run-syncdb

# Create superuser (admin account)
python manage.py createsuperuser
# Follow prompts to create admin account
```

#### Step 8: Run the Application

```cmd
# From cv_platform directory
python manage.py runserver
```

**Alternative (from project root)**:
```cmd
python run_app.py
```

#### Step 9: Access the Application

Open your browser and go to:
- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

### macOS Setup

#### Step 1: Install Python

**Option A: Using Homebrew (Recommended)**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11

# Verify installation
python3 --version
```

**Option B: Download from Website**
1. Download from https://www.python.org/downloads/
2. Run the installer
3. Follow on-screen instructions

#### Step 2: Install MongoDB

**Option A: Using Homebrew (Recommended)**
```bash
# Tap MongoDB formula
brew tap mongodb/brew

# Install MongoDB
brew install mongodb-community

# Start MongoDB service
brew services start mongodb-community

# Verify installation
mongosh
```

**Option B: Download DMG Installer**
1. Download from https://www.mongodb.com/try/download/community
2. Install using DMG file
3. Follow installation wizard

**Option C: MongoDB Atlas (Cloud)**
1. Go to https://www.mongodb.com/cloud/atlas
2. Create account and cluster
3. Get connection string

#### Step 3: Clone Project

```bash
# Using Git
git clone <repository-url>
cd cv-platform

# Or download manually and navigate to folder
cd ~/path/to/cv-platform
```

#### Step 4: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

#### Step 5: Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

#### Step 6: Configure Environment

Create `.env` file in project root:

```bash
# Create .env file
nano .env
```

Add the following content:
```env
COHERE_API_KEY=your-cohere-api-key-here
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB_NAME=cv_platform
DJANGO_SECRET_KEY=your-secret-key-here
```

Save (Ctrl+O, Enter, Ctrl+X)

#### Step 7: Initialize Database

```bash
# Navigate to cv_platform
cd cv_platform

# Run migrations
python manage.py migrate --run-syncdb

# Create superuser
python manage.py createsuperuser
```

#### Step 8: Run Application

**Method 1: Using Automated Script**
```bash
# From project root
chmod +x run_app.sh
./run_app.sh
```

**Method 2: Manual Start**
```bash
# From cv_platform directory
python manage.py runserver
```

#### Step 9: Access Application

- **Web App**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin/

---

### Linux Setup (Ubuntu/Debian)

#### Step 1: Install Python

```bash
# Update package manager
sudo apt update
sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-venv python3-pip -y

# Verify installation
python3 --version
```

#### Step 2: Install MongoDB

```bash
# Install MongoDB
sudo apt install -y mongodb

# Start MongoDB service
sudo systemctl start mongodb

# Enable auto-start
sudo systemctl enable mongodb

# Verify
mongosh
```

#### Step 3: Clone Project

```bash
git clone <repository-url>
cd cv-platform
```

#### Step 4: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 5: Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 6: Configure Environment

```bash
nano .env
```

Add:
```env
COHERE_API_KEY=your-api-key
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB_NAME=cv_platform
DJANGO_SECRET_KEY=your-secret-key
```

#### Step 7: Initialize Database

```bash
cd cv_platform
python manage.py migrate --run-syncdb
python manage.py createsuperuser
```

#### Step 8: Run Application

```bash
python manage.py runserver
```

---

## Quick Start

### Option 1: Automated Scripts (Easiest)

#### Windows:
```cmd
run_app.bat
```

#### macOS/Linux:
```bash
chmod +x INSTALL_AND_RUN.sh
./INSTALL_AND_RUN.sh
```

### Option 2: Python Script

```bash
# From project root (all platforms)
python run_app.py
```

This script automatically:
- ✓ Checks Python dependencies
- ✓ Verifies MongoDB connection
- ✓ Creates necessary directories
- ✓ Runs database migrations
- ✓ Offers to create admin user
- ✓ Starts the development server

### Option 3: Manual Steps

```bash
# Activate virtual environment
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Run migrations
cd cv_platform
python manage.py migrate --run-syncdb

# Create admin user (if needed)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

---

## Features & User Roles

### Student Features

**Dashboard Access**: http://127.0.0.1:8000/student/dashboard/

#### Capabilities:
1. **Upload CV**
   - Supports PDF and DOCX formats
   - Max file size: 10 MB
   - AI extracts: Name, Email, Phone, Skills, Education, Experience, etc.

2. **View Extracted Profile**
   - See all extracted CV data
   - Edit incorrect information
   - Update personal details

3. **Edit CV Data**
   - Modify education, experience, skills
   - Add certifications and languages
   - Update GPA and major

4. **Browse Other Students**
   - View public student profiles
   - See peer CVs and skills
   - Compare with other students

### Company Features

**Dashboard Access**: http://127.0.0.1:8000/company/dashboard/

#### Capabilities:
1. **Browse Students**
   - View all student profiles
   - Detailed candidate information
   - Contact information access

2. **Advanced Filtering**
   - Filter by GPA range
   - Filter by major/field of study
   - Filter by specific skills
   - Full-text search

3. **Compare Candidates**
   - Select 2-3 students
   - Side-by-side comparison
   - Skill matching analysis
   - Highlighting of best candidates

4. **Search**
   - Real-time search across all fields
   - Find candidates by name, skills, experience
   - Advanced filtering options

### Admin Features

**Dashboard Access**: http://127.0.0.1:8000/manage/dashboard/

#### Capabilities:
1. **User Management**
   - View all users (students, companies, admins)
   - Edit user information
   - Change user roles
   - Delete user accounts
   - Reset passwords

2. **Analytics Dashboard**
   - Total students and companies count
   - Most common skills
   - Major distribution charts
   - Average GPA statistics
   - User activity tracking

3. **CV Management**
   - View all CV profiles
   - Edit CV data
   - Delete specific CVs
   - Manage extracted information

4. **Django Admin Access**
   - http://127.0.0.1:8000/admin/
   - Full database management
   - User permissions
   - Group management

---

## Technology Stack

### Backend
- **Framework**: Django 4.2+
- **Language**: Python 3.8+
- **Database**: 
  - SQLite (user authentication)
  - MongoDB (CV profiles and data)
- **API Integration**: Cohere API
- **Web Server**: Django development server (use Gunicorn for production)

### Frontend
- **HTML/CSS**: Bootstrap 5.3
- **JavaScript**: Vanilla JavaScript + jQuery
- **Icons**: Bootstrap Icons 1.11+
- **Responsive**: Mobile, Tablet, Desktop

### Key Libraries

| Package | Version | Purpose |
|---------|---------|---------|
| Django | 4.2+ | Web framework |
| pymongo | 4.6+ | MongoDB connection |
| cohere | 5.0+ | AI API integration |
| pydantic | 2.0+ | Data validation |
| PyPDF2 | 3.0+ | PDF parsing |
| python-docx | 1.1+ | DOCX parsing |
| python-dotenv | 1.0+ | Environment variables |

---

## Configuration

### Environment Variables (.env)

Create a `.env` file in the project root with:

```env
# ===== REQUIRED =====

# Cohere API Key (generate at https://cohere.com)
COHERE_API_KEY=your-api-key-here

# ===== MONGODB =====

# MongoDB Connection String
# For local: mongodb://localhost:27017/
# For Atlas: mongodb+srv://user:password@cluster.mongodb.net/
MONGODB_URI=mongodb://localhost:27017/

# MongoDB Database Name
MONGODB_DB_NAME=cv_platform

# ===== DJANGO =====

# Secret key for Django (generate a random one)
DJANGO_SECRET_KEY=django-insecure-change-this-in-production

# Debug mode (False in production)
DEBUG=True

# Allowed hosts (comma-separated)
ALLOWED_HOSTS=localhost,127.0.0.1

# ===== OPTIONAL =====

# Application title
APP_TITLE=CV Platform

# Support email
SUPPORT_EMAIL=support@example.com
```

### Django Settings

**Key Configuration** in `cv_platform/settings.py`:

```python
# Language Support
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'),
    ('ar', 'العربية'),
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# File Upload
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760

# Internationalization
USE_I18N = True
USE_L10N = True
```

### MongoDB Connection

**Connection Methods:**

1. **Local MongoDB**:
   ```env
   MONGODB_URI=mongodb://localhost:27017/
   ```

2. **MongoDB Atlas (Cloud)**:
   ```env
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
   ```

3. **Custom Host**:
   ```env
   MONGODB_URI=mongodb://host:port/
   ```

---

## Usage Guide

### Initial Setup Checklist

- [ ] Python 3.8+ installed and in PATH
- [ ] Virtual environment created and activated
- [ ] Requirements installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with API keys
- [ ] MongoDB running locally or Atlas connection ready
- [ ] Database migrated (`python manage.py migrate --run-syncdb`)
- [ ] Superuser created (`python manage.py createsuperuser`)

### Creating Test Users

#### Via Django Admin

1. Go to http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Click "Users" in Accounts section
4. Click "Add User"
5. Fill in details and set role

#### Via Django Shell

```python
# Activate virtual environment first
python manage.py shell

from accounts.models import User

# Create student
student = User.objects.create_user(
    username='john_doe',
    email='john@example.com',
    password='secure_password_123',
    role='student'
)

# Create company
company = User.objects.create_user(
    username='tech_company',
    email='hr@company.com',
    password='company_password_123',
    role='company'
)

# Create admin
admin_user = User.objects.create_user(
    username='admin_user',
    email='admin@example.com',
    password='admin_password_123',
    role='admin'
)
admin_user.is_staff = True
admin_user.is_superuser = True
admin_user.save()

print("Users created successfully!")
exit()
```

### Student Workflow

1. **Register**
   - Go to http://127.0.0.1:8000/accounts/register/
   - Select "Student" role
   - Fill in form and submit

2. **Upload CV**
   - Go to http://127.0.0.1:8000/student/dashboard/
   - Click "Upload CV"
   - Select PDF or DOCX file
   - Wait for processing

3. **View Profile**
   - Check extracted CV data
   - Edit any incorrect information
   - Add missing details

### Company Workflow

1. **Register**
   - Go to http://127.0.0.1:8000/accounts/register/
   - Select "Company" role
   - Complete registration

2. **Browse Students**
   - Go to http://127.0.0.1:8000/company/dashboard/
   - View all available candidates

3. **Filter Students**
   - Use filters: GPA, Major, Skills
   - Perform text search
   - Narrow down candidates

4. **Compare Candidates**
   - Select 2-3 students
   - Click "Compare"
   - View side-by-side comparison
   - See scoring and recommendations

### Admin Workflow

1. **Access Dashboard**
   - Go to http://127.0.0.1:8000/manage/dashboard/
   - View analytics and statistics

2. **Manage Users**
   - View all users
   - Edit user information
   - Change roles
   - Delete accounts

3. **Manage CVs**
   - Edit CV profiles
   - Delete CV data
   - View CV details

4. **View Analytics**
   - Student and company counts
   - Skill distribution
   - Major statistics
   - GPA averages

---

## API & Data Schema

### User Roles

```python
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('company', 'Company'),
        ('admin', 'Administrator'),
    )
    
    username = CharField(max_length=150, unique=True)
    email = EmailField(unique=True)
    role = CharField(max_length=20, choices=ROLE_CHOICES)
    first_name = CharField(max_length=150)
    last_name = CharField(max_length=150)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
    date_joined = DateTimeField(auto_now_add=True)
```

### CV Profile Schema (Pydantic)

```python
class CVExtract(BaseModel):
    user_id: int
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    summary: Optional[str] = None
    skills: List[str] = []
    education: List[str] = []
    experience: List[str] = []
    certifications: List[str] = []
    languages: List[str] = []
    gpa: Optional[float] = None
    major: Optional[str] = None
    created_at: datetime
    updated_at: datetime
```

### MongoDB Document Example

```json
{
    "_id": ObjectId("..."),
    "user_id": 1,
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-0123",
    "summary": "Experienced software developer...",
    "skills": ["Python", "Django", "MongoDB", "React"],
    "education": [
        "BS Computer Science, University of Technology, 2022"
    ],
    "experience": [
        "Senior Developer at Tech Corp, 2022-Present"
    ],
    "certifications": ["AWS Certified Solutions Architect"],
    "languages": ["English", "Spanish"],
    "gpa": 3.8,
    "major": "Computer Science",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-20T14:45:00Z"
}
```

---

## Troubleshooting

### Common Issues & Solutions

#### 1. MongoDB Connection Error

**Error Message:**
```
pymongo.errors.ConnectionFailure: connection closed
```

**Solutions:**
- **Windows**: 
  - Check MongoDB Service: `Services` → find "MongoDB Server" → Start
  - Or run: `mongod` in Command Prompt
  
- **macOS**: 
  - Run: `brew services start mongodb-community`
  - Or: `mongod`
  
- **Linux**: 
  - Run: `sudo systemctl start mongodb`
  - Or: `sudo service mongodb start`

- **Check connection string in .env**:
  ```env
  MONGODB_URI=mongodb://localhost:27017/
  ```

#### 2. Cohere API Key Invalid

**Error Message:**
```
cohere.errors.CohereAPIError: Invalid API key
```

**Solutions:**
- Verify API key in `.env` file
- Generate new key at https://cohere.com/
- Ensure key is copied correctly (no extra spaces)
- Check API quota in Cohere dashboard

#### 3. File Upload Fails

**Errors:**
- "File too large"
- "Invalid file format"

**Solutions:**
- Max file size is 10 MB
- Only PDF and DOCX formats supported
- Ensure file is not corrupted
- Try with a different file

#### 4. Virtual Environment Issues

**Error:**
```
'python' is not recognized / command not found
```

**Solutions:**
- Windows: Run `venv\Scripts\activate`
- macOS/Linux: Run `source venv/bin/activate`
- Ensure you're in the correct directory
- Recreate venv: `python -m venv venv`

#### 5. Port 8000 Already in Use

**Error:**
```
Error: That port is already in use.
```

**Solutions:**
```bash
# Use different port
python manage.py runserver 8001

# Or kill process on port 8000
# Windows: netstat -ano | findstr :8000
# macOS/Linux: lsof -i :8000
```

#### 6. Static Files Not Loading

**Issue:**
- CSS and images not displaying

**Solutions:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Clear browser cache (Ctrl+Shift+Delete)

# Check file permissions
```

#### 7. Language Not Switching

**Issue:**
- Arabic/English switch not working

**Solutions:**
- Compile translations:
  ```bash
  python manage.py compilemessages
  ```
- Clear browser cookies
- Check `locale/` directory exists
- Restart server

#### 8. Migrations Error

**Error:**
```
No changes detected in app 'accounts'
```

**Solutions:**
```bash
# Force migrations
python manage.py migrate --run-syncdb

# Reset migrations (if needed - WARNING: deletes data)
python manage.py migrate accounts zero
python manage.py makemigrations accounts
python manage.py migrate accounts
```

#### 9. Permission Denied (macOS/Linux)

**Error:**
```
Permission denied: './run_app.sh'
```

**Solution:**
```bash
chmod +x run_app.sh
./run_app.sh
```

#### 10. Dependencies Installation Failed

**Error:**
```
ERROR: Could not install packages
```

**Solutions:**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Clear pip cache
pip cache purge

# Install one by one
pip install Django==4.2.0
pip install pymongo
# etc...

# Try with requirements in specific order
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Getting Help

1. Check the relevant guide:
   - Setup issues → Check INSTALL_AND_RUN.sh
   - User management → Check USER_MANAGEMENT_GUIDE.md
   - Arabic support → Check ARABIC_SUPPORT_GUIDE.md

2. Check Django logs:
   ```bash
   # See server output for error messages
   ```

3. Check MongoDB:
   ```bash
   mongosh  # Connect to MongoDB and verify data
   ```

4. Enable Django Debug Mode:
   - Set `DEBUG=True` in .env (development only)
   - See detailed error messages

---

## Advanced Topics

### Running on Production

#### Using Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn (from cv_platform directory)
gunicorn cv_platform.wsgi:application --bind 0.0.0.0:8000

# With multiple workers
gunicorn cv_platform.wsgi:application --workers 4 --bind 0.0.0.0:8000
```

#### Using Nginx

Create `/etc/nginx/sites-available/cv-platform`:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/staticfiles/;
    }
}
```

#### Environment Checklist for Production

- [ ] Set `DEBUG=False` in .env
- [ ] Generate strong `DJANGO_SECRET_KEY`
- [ ] Set proper `ALLOWED_HOSTS`
- [ ] Use HTTPS (SSL certificate)
- [ ] Use strong passwords
- [ ] Enable CORS if needed
- [ ] Set up database backups
- [ ] Use environment variables for secrets
- [ ] Enable logging and monitoring
- [ ] Use production database (PostgreSQL, MySQL)

### Using Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "run_app.py"]
```

Create `docker-compose.yml`:
```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - COHERE_API_KEY=${COHERE_API_KEY}
      - MONGODB_URI=mongodb://mongo:27017/
    depends_on:
      - mongo
  
  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
```

Run:
```bash
docker-compose up
```

### Custom Cohere Extraction Prompts

Edit `cv_extraction/cv_extractor.py` to modify the prompt:

```python
EXTRACTION_PROMPT = """
Extract the following information from the CV text:
1. Full Name
2. Email
3. Phone Number
4. Professional Summary
5. Skills (list)
6. Education (list)
7. Work Experience (list)
8. Certifications (list)
9. Languages (list)
10. GPA
11. Major

Provide output in JSON format.
"""
```

### Adding New Filters

Edit `cv_extraction/forms.py`:

```python
class StudentFilterForm(forms.Form):
    location = forms.CharField(required=False)
    years_experience = forms.IntegerField(required=False)
    salary_range = forms.ChoiceField(required=False)
```

### Database Backup

```bash
# MongoDB Backup
mongodump --db cv_platform --out backup_folder/

# SQLite Backup
cp db.sqlite3 db_backup_$(date +%Y%m%d).sqlite3
```

### Performance Optimization

1. **Enable Caching**:
   ```python
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
       }
   }
   ```

2. **Database Indexing**:
   ```python
   class CVProfile(models.Model):
       user = ForeignKey(User, on_delete=models.CASCADE)
       
       class Meta:
           indexes = [
               models.Index(fields=['user']),
           ]
   ```

3. **Query Optimization**:
   - Use `select_related()` and `prefetch_related()`
   - Avoid N+1 queries
   - Paginate large result sets

---

## Summary

### Quick Reference

| Task | Command |
|------|---------|
| Start app | `python run_app.py` |
| Run migrations | `python manage.py migrate --run-syncdb` |
| Create admin | `python manage.py createsuperuser` |
| Start MongoDB | `mongod` or `brew services start mongodb-community` |
| Activate venv | `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows) |
| Install packages | `pip install -r requirements.txt` |
| Django shell | `python manage.py shell` |
| Collect static files | `python manage.py collectstatic` |

### Key URLs

| Page | URL |
|------|-----|
| Home | http://127.0.0.1:8000/ |
| Login | http://127.0.0.1:8000/accounts/login/ |
| Register | http://127.0.0.1:8000/accounts/register/ |
| Student Dashboard | http://127.0.0.1:8000/student/dashboard/ |
| Company Dashboard | http://127.0.0.1:8000/company/dashboard/ |
| Admin Dashboard | http://127.0.0.1:8000/manage/dashboard/ |
| Django Admin | http://127.0.0.1:8000/admin/ |

---

## Additional Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **MongoDB Documentation**: https://docs.mongodb.com/
- **Cohere API**: https://docs.cohere.com/
- **Bootstrap Documentation**: https://getbootstrap.com/docs/
- **Python Virtual Environments**: https://docs.python.org/3/tutorial/venv.html

---

**Document Version**: 2.0  
**Last Updated**: November 2025  
**Status**: Complete & Production Ready

For issues or questions, refer to the specific guide or check Django documentation at https://docs.djangoproject.com/
