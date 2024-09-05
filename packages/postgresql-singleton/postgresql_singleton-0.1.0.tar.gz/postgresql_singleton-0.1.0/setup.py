from setuptools import setup, find_packages

setup(
    name="postgresql-singleton",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "psycopg2",
    ],
    description="PostgreSQL Singleton connection pool manager",
    author="song seung hwan",
    author_email="shdth117@gmail.com",
    url="https://github.com/yourusername/postgresql_client",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)