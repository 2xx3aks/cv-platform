# CV Platform - Django Application

A multi-role Django web application that uses Cohere AI to extract structured data from CVs, stores them in MongoDB, and provides role-based dashboards for students, companies, and administrators.

**Features:**
- 🌍 **Bilingual Support**: Arabic and English (العربية والإنجليزية)
- 🗄️ **MongoDB Database**: Full MongoDB integration (no SQLite)
- 🚀 **One-Click Startup**: Run entire application with a single script

## Features

### Student Features
- Upload CV (PDF or DOCX)
- View extracted profile
- View other students' public profiles

### Company Features
- Browse all student profiles
- Filter by GPA, major, skills, and full-text search
- Compare 2-3 students side-by-side
- Highlight strongest candidate based on scoring algorithm

### Admin Features
- Dashboard with analytics:
  - Total students and companies
  - Most common skills
  - Majors distribution
  - Average GPA
- Delete users and CV profiles
- Full Django admin access

## Technology Stack

- **Backend**: Django 4.2+
- **Database**: MongoDB (full integration via djongo)
- **AI Extraction**: Cohere API
- **Frontend**: Bootstrap 5
- **File Processing**: PyPDF2, python-docx
- **Internationalization**: Django i18n (Arabic & English)

## Quick Start (One Command)

### Windows:
```bash
run_app.bat
```

### Linux/Mac:
```bash
chmod +x run_app.sh
./run_app.sh
```

### Python (All Platforms):
```bash
python run_app.py
```

The script will:
- ✓ Check MongoDB connection
- ✓ Create necessary directories
- ✓ Check environment variables
- ✓ Run database migrations
- ✓ Start the Django server

## Manual Installation

1. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Create .env file with:
COHERE_API_KEY=your-cohere-api-key-here
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB_NAME=cv_platform
DJANGO_SECRET_KEY=your-secret-key-here
```

4. **Ensure MongoDB is running**
```bash
# Windows: MongoDB service should be running
# Linux/Mac: sudo systemctl start mongod
```

5. **Run the startup script**
```bash
python run_app.py
```

6. **Access the application**
- Web interface: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## MongoDB Setup

**Important**: This application uses MongoDB as the primary database (not SQLite).

Make sure MongoDB is running on your system:

```bash
# On Windows (if installed as service, it should start automatically)
# Or start manually:
mongod

# On Linux/Mac:
sudo systemctl start mongod
# or
mongod
```

The application will automatically connect to MongoDB using the `MONGODB_URI` from your `.env` file.

## Language Support

The application supports **Arabic (العربية)** and **English**:

- Language switcher is available in the navigation bar
- All pages automatically adjust text direction (RTL for Arabic, LTR for English)
- Translations can be extended by editing files in `locale/` directory

To add more translations:
```bash
python create_translations.py
# Edit .po files in locale/
python cv_platform/manage.py compilemessages
```

## Usage

### For Students

1. Register with role "student"
2. Login and navigate to "Upload CV"
3. Upload your CV (PDF or DOCX)
4. View your extracted profile on the dashboard

### For Companies

1. Register with role "company"
2. Login to see the student browsing dashboard
3. Use filters to find candidates:
   - GPA range
   - Major
   - Skills (comma-separated)
   - Full-text search
4. Click "Compare" to select 2-3 students for side-by-side comparison

### For Admins

1. Create an admin account via Django admin or set role to "admin" for a user
2. Access admin dashboard for analytics
3. Use Django admin panel for detailed management

## Project Structure

```
cv_platform/
├── cv_platform/          # Main Django project
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL configuration
│   └── manage.py         # Django management script
├── accounts/             # User authentication app
│   ├── models.py         # Custom User model with role
│   ├── views.py          # Auth views
│   └── forms.py          # Registration form
├── cv_extraction/        # CV processing app
│   ├── schemas.py        # Pydantic CVExtract schema
│   ├── cv_extractor.py   # Cohere extraction service
│   ├── mongodb_utils.py  # MongoDB operations
│   ├── views.py          # Role-based views
│   └── forms.py          # CV upload and filter forms
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── accounts/         # Auth templates
│   └── cv_extraction/    # App templates
├── static/               # Static files (CSS, JS)
├── media/                # Uploaded files
└── requirements.txt      # Python dependencies
```

## CV Extraction Schema

All extracted CVs follow this Pydantic schema:

```python
class CVExtract(BaseModel):
    full_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    summary: Optional[str]
    skills: List[str]
    education: List[str]
    experience: List[str]
    certifications: List[str]
    languages: List[str]
    gpa: Optional[float]
    major: Optional[str]
```

## MongoDB Document Structure

```json
{
  "user_id": 1,
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "summary": "Experienced software developer...",
  "skills": ["Python", "Django", "MongoDB"],
  "education": ["BS Computer Science, University X"],
  "experience": ["Software Developer at Company Y"],
  "certifications": ["AWS Certified"],
  "languages": ["English", "Spanish"],
  "gpa": 3.8,
  "major": "Computer Science",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

## Role-Based Redirects

After login, users are redirected based on their role:
- **Student** → Student Dashboard
- **Company** → Company Dashboard (Student List)
- **Admin** → Admin Dashboard

## Development Notes

- The application uses SQLite for Django's user management
- CV profiles are stored in MongoDB
- Cohere API is used for structured extraction from CV text
- All pages are responsive using Bootstrap 5
- File uploads are limited to 10MB

## Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB is running: `mongod` or check service status
- Verify `MONGODB_URI` in `.env` file

### Cohere API Error
- Verify `COHERE_API_KEY` is set in `.env`
- Check API key validity and quota

### File Upload Issues
- Ensure `media/` directory exists and is writable
- Check file size (max 10MB)
- Verify file format (PDF or DOCX only)

## License

This project is provided as-is for educational and development purposes.

