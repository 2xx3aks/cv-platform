#!/usr/bin/env python
"""
Complete startup script for CV Platform Django application.
This script:
1. Checks MongoDB connection
2. Creates necessary directories
3. Runs migrations
4. Starts the Django development server
"""
import os
import sys
import subprocess
import time
from pathlib import Path

# Try importing dependencies (will check later)
try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
except ImportError:
    MongoClient = None
    ConnectionFailure = None

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Load environment variables (if dotenv available)
try:
    load_dotenv()
except:
    pass

BASE_DIR = Path(__file__).resolve().parent
CV_PLATFORM_DIR = BASE_DIR / 'cv_platform'

def print_step(step_num, message):
    """Print formatted step message."""
    print(f"\n{'='*60}")
    print(f"Step {step_num}: {message}")
    print('='*60)

def check_mongodb():
    """Check if MongoDB is running."""
    print_step(1, "Checking MongoDB Connection")
    
    if MongoClient is None:
        print("⚠ pymongo not installed - skipping MongoDB check")
        return False
    
    mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    
    try:
        # Extract host and port from URI
        if '://' in mongodb_uri:
            uri_parts = mongodb_uri.split('://')[1]
            if '/' in uri_parts:
                host_part = uri_parts.split('/')[0]
            else:
                host_part = uri_parts
            if ':' in host_part:
                host, port = host_part.split(':')
                port = int(port)
            else:
                host = host_part
                port = 27017
        else:
            host = 'localhost'
            port = 27017
        
        client = MongoClient(host, port, serverSelectionTimeoutMS=2000)
        client.server_info()  # Force connection
        print(f"✓ MongoDB is running at {host}:{port}")
        return True
    except ConnectionFailure:
        print(f"✗ MongoDB connection failed at {host}:{port}")
        print("  Please ensure MongoDB is running:")
        print("  - Windows: Check MongoDB service or run 'mongod'")
        print("  - Linux/Mac: Run 'sudo systemctl start mongod' or 'mongod'")
        return False
    except Exception as e:
        print(f"✗ Error connecting to MongoDB: {e}")
        return False

def create_directories():
    """Create necessary directories."""
    print_step(2, "Creating Directories")
    directories = [
        BASE_DIR / 'static',
        BASE_DIR / 'staticfiles',
        BASE_DIR / 'media',
        BASE_DIR / 'locale',
    ]
    
    for directory in directories:
        directory.mkdir(exist_ok=True)
        print(f"✓ Created/verified: {directory}")

def check_environment():
    """Check environment variables."""
    print_step(3, "Checking Environment Variables")
    
    required_vars = ['COHERE_API_KEY']
    missing = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing.append(var)
            print(f"✗ Missing: {var}")
        else:
            print(f"✓ Found: {var}")
    
    if missing:
        print(f"\n⚠ Warning: Missing required environment variables: {', '.join(missing)}")
        print("  Please set them in your .env file")
        response = input("  Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Optional variables
    optional_vars = {
        'MONGODB_URI': 'mongodb://localhost:27017/',
        'MONGODB_DB_NAME': 'cv_platform',
        'DJANGO_SECRET_KEY': 'django-insecure-change-this-in-production'
    }
    
    for var, default in optional_vars.items():
        value = os.getenv(var, default)
        print(f"✓ {var}: {value}")

def run_migrations():
    """Run Django migrations."""
    print_step(4, "Running Database Migrations")
    
    # Add parent directory to Python path
    if str(BASE_DIR) not in sys.path:
        sys.path.insert(0, str(BASE_DIR))
    
    os.chdir(CV_PLATFORM_DIR)
    
    try:
        # Make migrations
        print("Running makemigrations...")
        env = os.environ.copy()
        env['PYTHONPATH'] = str(BASE_DIR)
        result = subprocess.run(
            [sys.executable, 'manage.py', 'makemigrations'],
            capture_output=True,
            text=True,
            timeout=30,
            env=env
        )
        if result.returncode == 0:
            print("✓ Migrations created")
            if result.stdout:
                print(f"  {result.stdout.strip()}")
        else:
            if result.stdout:
                print(f"⚠ {result.stdout.strip()}")
            if result.stderr:
                print(f"⚠ {result.stderr.strip()}")
            print("  Note: Some warnings are normal")
        
        # Run migrations
        print("\nRunning migrate...")
        env = os.environ.copy()
        env['PYTHONPATH'] = str(BASE_DIR)
        result = subprocess.run(
            [sys.executable, 'manage.py', 'migrate', '--run-syncdb'],
            capture_output=True,
            text=True,
            timeout=60,
            env=env
        )
        if result.returncode == 0:
            print("✓ Migrations applied")
        else:
            if result.stdout:
                print(f"⚠ {result.stdout.strip()}")
            if result.stderr:
                print(f"⚠ {result.stderr.strip()}")
            print("  Note: Some migration errors may occur with MongoDB/djongo")
            print("  The application may still work - CV profiles use MongoDB directly")
        
    except subprocess.TimeoutExpired:
        print("⚠ Migration timed out - continuing anyway")
    except Exception as e:
        print(f"⚠ Migration error: {e}")
        print("  Continuing - application may still work")

def create_superuser_check():
    """Check if superuser exists, offer to create one."""
    print_step(5, "Checking for Admin User")
    
    # Add parent directory to Python path
    if str(BASE_DIR) not in sys.path:
        sys.path.insert(0, str(BASE_DIR))
    
    os.chdir(CV_PLATFORM_DIR)
    
    try:
        env = os.environ.copy()
        env['PYTHONPATH'] = str(BASE_DIR)
        result = subprocess.run(
            [sys.executable, 'manage.py', 'shell', '-c', 
             'from accounts.models import User; print("exists" if User.objects.filter(is_superuser=True).exists() else "none")'],
            capture_output=True,
            text=True,
            env=env
        )
        
        if 'exists' in result.stdout:
            print("✓ Admin user exists")
        else:
            print("⚠ No admin user found")
            response = input("  Create superuser now? (y/n): ")
            if response.lower() == 'y':
                env = os.environ.copy()
                env['PYTHONPATH'] = str(BASE_DIR)
                subprocess.run([sys.executable, 'manage.py', 'createsuperuser'], env=env)
    except Exception as e:
        print(f"⚠ Could not check admin user: {e}")

def start_server():
    """Start Django development server."""
    print_step(6, "Starting Django Development Server")
    
    # Add parent directory to Python path
    if str(BASE_DIR) not in sys.path:
        sys.path.insert(0, str(BASE_DIR))
    
    os.chdir(CV_PLATFORM_DIR)
    
    print("\n" + "="*60)
    print("🚀 Starting Django Server...")
    print("="*60)
    print("\nServer will be available at:")
    print("  - Web Interface: http://127.0.0.1:8000/")
    print("  - Admin Panel: http://127.0.0.1:8000/admin/")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        env = os.environ.copy()
        env['PYTHONPATH'] = str(BASE_DIR)
        subprocess.run([sys.executable, 'manage.py', 'runserver'], env=env)
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped by user")
    except Exception as e:
        print(f"\n✗ Error starting server: {e}")
        sys.exit(1)

def check_dependencies():
    """Check if required Python packages are installed."""
    print_step(0, "Checking Python Dependencies")
    
    required_packages = ['django', 'pymongo', 'cohere', 'pydantic']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} installed")
        except ImportError:
            missing.append(package)
            print(f"✗ {package} NOT installed")
    
    if missing:
        print(f"\n⚠ Missing packages: {', '.join(missing)}")
        print("  Please install dependencies:")
        print("  pip install -r requirements.txt")
        response = input("\n  Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    return len(missing) == 0

def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("CV Platform - Django Application Startup")
    print("="*60)
    
    # Check dependencies first
    deps_ok = check_dependencies()
    if not deps_ok:
        print("\n⚠ Some dependencies are missing. The application may not work correctly.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Check MongoDB
    if not check_mongodb():
        print("\n⚠ MongoDB is not running. Some features may not work.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Check environment
    check_environment()
    
    # Run migrations
    run_migrations()
    
    # Check/create superuser
    create_superuser_check()
    
    # Start server
    start_server()

if __name__ == '__main__':
    main()

