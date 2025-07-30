#!/usr/bin/env python3
"""Setup script to ensure demo environment is ready."""

import sys
import subprocess
import importlib
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True


def check_dependencies():
    """Check if all required packages are installed."""
    required_packages = [
        'fastapi',
        'uvicorn',
        'ray',
        'torch',
        'transformers',
        'pydantic',
        'numpy',
        'requests'
    ]
    
    missing = []
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} - OK")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing.append(package)
    
    return missing


def check_file_structure():
    """Check if all necessary files exist."""
    required_files = [
        'main.py',
        'src/api/main.py',
        'src/services/ray_serve.py',
        'ui/index.html',
        'ui/app.js',
        'serve_ui.py',
        'demo_interview.py',
        'start_demo.sh',
        'stop_demo.sh'
    ]
    
    missing = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} - OK")
        else:
            print(f"❌ {file_path} - Missing")
            missing.append(file_path)
    
    return missing


def check_ports():
    """Check if required ports are available."""
    import socket
    
    ports = [8000, 3000, 8265]
    busy_ports = []
    
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            print(f"⚠️  Port {port} - In use")
            busy_ports.append(port)
        else:
            print(f"✅ Port {port} - Available")
    
    return busy_ports


def install_missing_packages(missing_packages):
    """Install missing packages."""
    if not missing_packages:
        return True
    
    print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-e', '.'
        ])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def main():
    """Main setup function."""
    print("🔧 MLServe Demo Setup Check")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print("\n📦 Checking Dependencies:")
    missing_deps = check_dependencies()
    
    print("\n📁 Checking File Structure:")
    missing_files = check_file_structure()
    
    print("\n🔌 Checking Ports:")
    busy_ports = check_ports()
    
    # Summary
    print("\n" + "=" * 40)
    print("📋 Setup Summary:")
    
    if missing_files:
        print(f"❌ Missing files: {len(missing_files)}")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease ensure all project files are present!")
        sys.exit(1)
    
    if missing_deps:
        print(f"⚠️  Missing dependencies: {len(missing_deps)}")
        print("Attempting to install...")
        if not install_missing_packages(missing_deps):
            sys.exit(1)
    
    if busy_ports:
        print(f"⚠️  Ports in use: {busy_ports}")
        print("You may need to stop other services or the demo might not start properly.")
    
    print("\n🎉 Setup Check Complete!")
    print("\n🚀 Ready to start demo:")
    print("   ./start_demo.sh")
    print("\n📖 Or run individual components:")
    print("   python main.py        # Start API")
    print("   python serve_ui.py    # Start UI")
    print("   python demo_interview.py  # Command demo")


if __name__ == "__main__":
    main()