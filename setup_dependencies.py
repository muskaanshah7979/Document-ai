import importlib
import subprocess
import sys

REQUIRED_PACKAGES = [
    "python-dateutil",
    "streamlit",
   
]

def install_package(package):
    """Install a package using pip."""
    print(f"Checking {package}...")
    try:
        importlib.import_module(package.split("-")[0])
        print(f" {package} already installed")
    except ImportError:
        print(f" Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f" {package} installed successfully")

def main():
    for pkg in REQUIRED_PACKAGES:
        install_package(pkg)

if __name__ == "__main__":
    main()