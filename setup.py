from setuptools import setup, find_packages

setup(
    name="thinkalike",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "fastapi>=0.95.0",
        "uvicorn>=0.21.1",
        "sqlalchemy>=2.0.9",
        "alembic>=1.10.3",
        "python-dotenv>=1.0.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "pydantic[email]>=1.10.7",
        "psycopg2-binary>=2.9.6",
        "python-multipart>=0.0.6",
    ],
)
