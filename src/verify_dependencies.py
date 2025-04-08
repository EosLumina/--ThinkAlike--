import subprocess
import sys

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except Exception as e:
        print(f"Failed to install {package}: {e}")

try:
    import altair
except ImportError:
    print("Installing 'altair'...")
    install_package("altair")

try:
    import pandas
except ImportError:
    print("Installing 'pandas'...")
    install_package("pandas")

try:
    import great_expectations
except ImportError:
    print("Installing 'great_expectations'...")
    install_package("great-expectations")

try:
    import tensorflow
except ImportError:
    print("Installing 'tensorflow'...")
    install_package("tensorflow")

try:
    import torch
except ImportError:
    print("Installing 'torch'...")
    install_package("torch")

print("Dependency check completed.")
