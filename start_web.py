#!/usr/bin/env python3
"""
Deep Live Cam - Web Version
A simple startup script for the face swap web application
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'flask', 'opencv-python', 'numpy', 'pillow', 'flask-cors'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print(f"   pip install -r web_requirements.txt")
        return False
    
    return True

def main():
    print("🚀 Starting Deep Live Cam Web Application...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("✅ All dependencies found!")
    print("🌐 Starting web server...")
    print("🔗 Open your browser and go to: http://localhost:5000")
    print("⚠️  Allow camera access when prompted")
    print("=" * 50)
    
    # Import and run the Flask app
    try:
        from app import app
        app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()