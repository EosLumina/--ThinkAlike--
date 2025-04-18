from setuptools import setup, find_packages

setup(
    name="ThinkAlike",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Add dependencies from requirements.txt here
        # e.g., 'fastapi', 'uvicorn', 'sqlalchemy', etc.
        # It's often better to manage dependencies via requirements.txt
        # and use pip install -r requirements.txt
    ],
    entry_points={
        'console_scripts': [
            'thinkalike=manage:main', # Example if manage.py has a main function
        ],
    },
    # Add other metadata like author, description, etc.
    author="Your Name",
    author_email="your.email@example.com",
    description="ThinkAlike platform - Architecting Connection for Enlightenment 2.0",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/ThinkAlike", # Replace with your repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", # Choose appropriate license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
