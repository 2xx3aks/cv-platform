#!/bin/bash
# Complete installation, setup, and run script for macOS/Linux (with admin creation)

echo "============================================================"
echo "CV Platform - Complete Setup and Run (macOS/Linux)"
echo "============================================================"
echo ""

# ---------------------------
# Step 0: Check Python
# ---------------------------
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from https://www.python.org/"
    echo "Or install via Homebrew: brew install python3"
    exit 1
fi

echo "Python version:"
python3 --version
echo ""

# ---------------------------
# Step 1: Install dependencies
# ---------------------------
echo "Step 1: Installing Python Dependencies..."
echo ""
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo ""
    echo "WARNING: Some packages may have failed to install"
    echo "You may need to install them manually"
    read -p "Press Enter to continue..."
fi
echo ""

# ---------------------------
# Step 2: Check .env file
# ---------------------------
echo "Step 2: Checking for .env file..."
if [ ! -f .env ]; then
    echo ""
    echo "WARNING: .env file not found!"
    echo "Please create a .env file with:"
    echo "   COHERE_API_KEY=your-key-here"
    echo "   MONGODB_URI=mongodb://localhost:27017/"
    echo "   MONGODB_DB_NAME=cv_platform"
    echo "   DJANGO_SECRET_KEY=your-secret-key"
    echo ""
    read -p "Press Enter to continue..."
fi
echo ""

# ---------------------------
# Step 3: Check MongoDB
# ---------------------------
echo "Step 3: Checking MongoDB..."
if command -v mongosh &> /dev/null; then
    echo "✓ MongoDB tools found"
    echo "Make sure MongoDB is running: brew services start mongodb-community"
elif command -v mongo &> /dev/null; then
    echo "✓ MongoDB tools found"
    echo "Make sure MongoDB is running: brew services start mongodb-community"
else
    echo "⚠ MongoDB tools not found locally"
    echo "Install via Homebrew: brew tap mongodb/brew && brew install mongodb-community"
fi
echo ""

# ---------------------------
# Step 4: Create Admin User
# ---------------------------
echo "Step 4: Creating Admin User..."
python3 - <<'EOF'
import os
from pymongo import MongoClient
import hashlib

mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
db_name = os.getenv("MONGODB_DB_NAME", "cv_platform")

client = MongoClient(mongo_uri)
db = client[db_name]
users = db["users"]

if users.find_one({"role": "admin"}):
    print("✓ Admin already exists")
else:
    def hash_password(pwd):
        return hashlib.sha256(pwd.encode()).hexdigest()

    admin_doc = {
        "name": "Admin",
        "email": "admin@cv.com",
        "password": hash_password("admin123"),
        "role": "admin",
        "active": True,
    }

    users.insert_one(admin_doc)
    print("✓ Admin created successfully: admin@cv.com / admin123")
EOF
echo ""

# ---------------------------
# Step 5: Start Application
# ---------------------------
echo "Step 5: Starting Application..."
echo ""
python3 run_app.py
