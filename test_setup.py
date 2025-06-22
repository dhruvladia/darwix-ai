#!/usr/bin/env python
"""
Test script to verify the environment setup for Darwix AI Assessment.
Run this before starting the Django server.
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8+"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} - Please use Python 3.8+")
        return False

def check_packages():
    """Check if required packages are installed"""
    print("\nChecking required packages...")
    packages = {
        'django': 'Django',
        'dotenv': 'python-dotenv',
        'requests': 'requests',
        'gunicorn': 'gunicorn',
        'sarvamai': 'sarvamai'
    }
    
    all_installed = True
    for module, package in packages.items():
        try:
            __import__(module)
            print(f"✓ {package} - Installed")
        except ImportError:
            print(f"✗ {package} - Not installed")
            all_installed = False
    
    return all_installed

def check_env_file():
    """Check if .env file exists and has required keys"""
    print("\nChecking environment variables...")
    env_path = Path('.env')
    
    if not env_path.exists():
        print("✗ .env file not found - Please create it with your API keys")
        print("\nCreate a .env file with:")
        print('SARVAM_AI_API_KEY="YOUR_SARVAM_AI_API_KEY_HERE"')
        print('OPENROUTER_API_KEY="YOUR_OPENROUTER_API_KEY_HERE"')
        return False
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    sarvam_key = os.getenv('SARVAM_AI_API_KEY')
    openrouter_key = os.getenv('OPENROUTER_API_KEY')
    
    env_ok = True
    
    if sarvam_key and sarvam_key != "YOUR_SARVAM_AI_API_KEY_HERE":
        print("✓ SARVAM_AI_API_KEY - Set")
    else:
        print("✗ SARVAM_AI_API_KEY - Not set or using placeholder")
        env_ok = False
    
    if openrouter_key and openrouter_key != "YOUR_OPENROUTER_API_KEY_HERE":
        print("✓ OPENROUTER_API_KEY - Set")
    else:
        print("✗ OPENROUTER_API_KEY - Not set or using placeholder")
        env_ok = False
    
    return env_ok

def check_django_setup():
    """Check Django project structure"""
    print("\nChecking Django project structure...")
    
    required_files = [
        'manage.py',
        'darwix_project/settings.py',
        'ai_features_app/views.py',
        'templates/index.html'
    ]
    
    all_files_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path} - Found")
        else:
            print(f"✗ {file_path} - Not found")
            all_files_exist = False
    
    return all_files_exist

def main():
    """Run all checks"""
    print("=" * 50)
    print("Darwix AI Assessment - Environment Check")
    print("=" * 50)
    
    checks = [
        check_python_version(),
        check_packages(),
        check_env_file(),
        check_django_setup()
    ]
    
    print("\n" + "=" * 50)
    if all(checks):
        print("✓ All checks passed! You're ready to run the Django server.")
        print("\nNext steps:")
        print("1. Run migrations: python manage.py migrate")
        print("2. Start server: python manage.py runserver")
        print("3. Open browser: http://127.0.0.1:8000/")
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        if not checks[1]:  # Package check failed
            print("\nInstall missing packages with: pip install -r requirements.txt")
    print("=" * 50)

if __name__ == '__main__':
    main() 