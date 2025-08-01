#!/usr/bin/env python3
"""
Quick launcher for the Organizational Digital Twin simulation.
This script helps users start the application with proper setup verification.
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if required packages are installed"""
    try:
        import streamlit
        import openai
        import plotly
        import pandas
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists with OpenAI API key"""
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("Please create a .env file with your OpenAI API key")
        print("See SETUP.md for detailed instructions")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
        if 'OPENAI_API_KEY=' not in content or 'your_openai_api_key_here' in content:
            print("❌ OpenAI API key not configured in .env file")
            print("Please add your actual OpenAI API key to the .env file")
            return False
    
    print("✅ Environment configuration found")
    return True

def main():
    """Main launcher function"""
    print("🏢 Organizational Digital Twin Launcher")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    print(f"✅ Python {sys.version}")
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment
    if not check_env_file():
        sys.exit(1)
    
    print("\n🚀 Starting Organizational Digital Twin...")
    print("The application will open in your browser at http://localhost:8501")
    print("Press Ctrl+C to stop the simulation")
    print("=" * 50)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Simulation stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 