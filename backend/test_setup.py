"""
Quick setup verification script.
Run this to check if your environment is configured correctly.
"""
import os
import sys

def check_python_version():
    """Check if Python version is 3.10+"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python version: {version.major}.{version.minor}.{version.micro} (need 3.10+)")
        return False

def check_api_key():
    """Check if GEMINI_API_KEY is set"""
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and len(api_key) > 10:
        print(f"✓ GEMINI_API_KEY is set (length: {len(api_key)})")
        return True
    else:
        print("✗ GEMINI_API_KEY is not set or invalid")
        print("  Set it with: set GEMINI_API_KEY=your_key_here")
        print("  Get key from: https://aistudio.google.com/app/apikey")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required = [
        "fastapi",
        "uvicorn",
        "google.generativeai",
        "PIL",
        "pydantic"
    ]
    
    all_installed = True
    for package in required:
        try:
            if package == "PIL":
                __import__("PIL")
            elif package == "google.generativeai":
                __import__("google.generativeai")
            else:
                __import__(package)
            print(f"✓ {package} installed")
        except ImportError:
            print(f"✗ {package} not installed")
            all_installed = False
    
    if not all_installed:
        print("\nInstall missing packages with:")
        print("  pip install -r requirements.txt")
    
    return all_installed

def main():
    print("=" * 50)
    print("Second Brain Setup Verification")
    print("=" * 50)
    print()
    
    checks = [
        check_python_version(),
        check_api_key(),
        check_dependencies()
    ]
    
    print()
    print("=" * 50)
    if all(checks):
        print("✓ All checks passed! You're ready to go.")
        print("\nStart the server with:")
        print("  python main.py")
    else:
        print("✗ Some checks failed. Please fix the issues above.")
    print("=" * 50)

if __name__ == "__main__":
    main()
