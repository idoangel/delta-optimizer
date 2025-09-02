#!/usr/bin/env python3
"""
DeltaOptimizer Build and Installation Script
One-click setup for distribution and local installation.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a shell command with error handling."""
    print(f"🚀 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def clean_build_files():
    """Remove previous build files."""
    build_dirs = ['build', 'dist', 'delta_optimizer.egg-info']
    for dir_name in build_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 Removed {dir_name}/")

def build_package():
    """Build the Python package."""
    commands = [
        "python setup.py sdist bdist_wheel",
        "python -m build"
    ]
    
    for cmd in commands:
        if not run_command(cmd, "Building package"):
            return False
    return True

def install_locally():
    """Install the package locally for testing."""
    return run_command("pip install .", "Installing package locally")

def upload_to_pypi():
    """Upload to PyPI (requires twine and credentials)."""
    print("📤 Uploading to PyPI...")
    print("Note: Make sure you have:")
    print("1. twine installed: pip install twine")
    print("2. PyPI credentials in ~/.pypirc")
    print("3. Package version updated in setup.py")
    
    response = input("Continue with upload? (y/N): ")
    if response.lower() != 'y':
        print("Upload cancelled")
        return False
    
    return run_command("twine upload dist/*", "Uploading to PyPI")

def run_tests():
    """Run quick validation tests."""
    tests = [
        "python -c \"import delta_optimizer; print('✅ Import successful')\"",
        "python -c \"from delta_optimizer import DeltaOptimizer; print('✅ DeltaOptimizer import successful')\"",
        "python examples/quick_start.py --dry-run"
    ]
    
    for test in tests:
        if not run_command(test, "Running validation test"):
            return False
    return True

def create_zip_package():
    """Create a ZIP file for easy distribution."""
    import zipfile
    from datetime import datetime
    
    zip_filename = f"delta-optimizer-{datetime.now().strftime('%Y%m%d')}.zip"
    files_to_include = [
        'delta_optimizer/',
        'examples/',
        'setup.py',
        'requirements.txt',
        'README.md',
        'LICENSE',
        'build_and_install.py'
    ]
    
    print(f"📦 Creating {zip_filename}...")
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for item in files_to_include:
            if os.path.exists(item):
                if os.path.isdir(item):
                    for root, dirs, files in os.walk(item):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, os.path.dirname(item))
                            zipf.write(file_path, arcname)
                else:
                    zipf.write(item)
    
    print(f"✅ Created {zip_filename}")
    return zip_filename

def main():
    """Main installation and build menu."""
    print("=" * 50)
    print("DeltaOptimizer Build and Installation System")
    print("=" * 50)
    
    options = {
        '1': ("Clean build files", clean_build_files),
        '2': ("Build package", build_package),
        '3': ("Install locally", install_locally),
        '4': ("Run tests", run_tests),
        '5': ("Create ZIP package", create_zip_package),
        '6': ("Upload to PyPI", upload_to_pypi),
        '7': ("Full pipeline (clean+build+install+test)", lambda: (
            clean_build_files() and 
            build_package() and 
            install_locally() and 
            run_tests()
        )),
        '8': ("Exit", sys.exit)
    }
    
    while True:
        print("\n📋 Available options:")
        for key, (description, _) in options.items():
            print(f"  {key}. {description}")
        
        choice = input("\nSelect an option (1-8): ").strip()
        
        if choice in options:
            description, function = options[choice]
            print(f"\n{'='*30}")
            print(f"Running: {description}")
            print(f"{'='*30}")
            function()
        else:
            print("❌ Invalid option. Please choose 1-8.")

if __name__ == "__main__":
    # Add current directory to Python path
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    # Check if we're in the right directory
    if not (current_dir / "setup.py").exists():
        print("❌ Error: setup.py not found. Please run this script from the package root directory.")
        sys.exit(1)
    
    main()