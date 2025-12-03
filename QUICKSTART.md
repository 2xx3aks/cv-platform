# Quick Start Guide - Updated

## Prerequisites

- Python 3.8+
- MongoDB installed and running
- Cohere API key

## One-Command Startup


## Mac:
```bash
chmod +x run_app.sh
./run_app.sh
```

### Python (All Platforms):
```bash
python run_app.py
```

The `run_app.py` script automatically:
1. ✓ Checks MongoDB connection
2. ✓ Creates necessary directories
3. ✓ Validates environment variables
4. ✓ Runs database migrations
5. ✓ Starts Django server

## Setup Steps

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Create environment file (.env)**
```bash
COHERE_API_KEY=your-cohere-api-key-here
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB_NAME=cv_platform
DJANGO_SECRET_KEY=your-secret-key-here
```

3. **Start MongoDB** (if not running)
```bash
# Linux/Mac: sudo systemctl start mongod
```

4. **Run the application**
```bash
python run_app.py
```

## Language Support

The application supports **Arabic** and **English**:
- Use the language switcher in the navigation bar
- Pages automatically adjust direction (RTL/LTR)
- All UI elements are translated

## MongoDB Configuration

**Important**: This app uses MongoDB as the primary database (not SQLite).

- All user data and CV profiles are stored in MongoDB
- Connection string: `MONGODB_URI` in `.env`
- Database name: `MONGODB_DB_NAME` in `.env`

## First Steps

1. **Register a student account**
   - Go to Register → Select "Student"
   - Upload a CV (PDF or DOCX)

2. **Register a company account**
   - Go to Register → Select "Company"
   - Browse and filter students

3. **Admin access**
   - Create superuser via Django admin
   - Access admin dashboard for analytics

## Troubleshooting

### MongoDB Connection Error
```bash
# Check if MongoDB is running
mongo

# Start MongoDB
sudo systemctl start mongod
```

### djongo Installation Issues
If djongo has issues, the app will still work for CV profiles (stored in MongoDB via pymongo). User authentication uses Django's default database adapter.

### Language Not Switching
- Clear browser cache
- Check that `locale/` directory exists
- Run: `python cv_platform/manage.py compilemessages`

## Project Structure

```
cv_platform/
├── cv_platform/       # Main project
├── accounts/          # User management (MongoDB)
├── cv_extraction/     # CV processing (MongoDB)
├── templates/         # HTML templates (i18n)
├── locale/            # Translation files
├── static/            # Static files
├── media/             # Uploaded files
├── run_app.py         # Main startup script
└── run_app.sh         # Linux/Mac startup
```

## Next Steps

- Customize translations in `locale/`
- Adjust extraction prompts in `cv_extraction/cv_extractor.py`
- Add more filters in `cv_extraction/forms.py`
- Extend analytics in `cv_extraction/views.py`
