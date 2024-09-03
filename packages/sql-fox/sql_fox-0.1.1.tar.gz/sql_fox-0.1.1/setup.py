from setuptools import setup, find_packages

setup(
    name='sql-fox',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        "pymysql>=1.0.2",
        "sqlalchemy>=1.4.0",
        "cryptography>=3.4.7",
        "cffi>=1.14.5",
        "colorama>=0.4.4",
        "cx-oracle>=8.1.0",
        "fdb>=2.0.0",
        "future>=0.18.2",
        "greenlet>=1.1.0",
        "loguru>=0.5.3",
        "packaging>=20.9",
        "pluggy>=0.13.1",
        "psycopg2>=2.8.6",
        "pycparser>=2.20",
        "pyodbc>=4.0.30",
        "typing-extensions>=3.7.4.3",
        "win32-setctime>=1.0.2"
    ],
    author='russkiylis',
    author_email='diaminerr@yandex.ru',
    description='An easy way to work with your database.',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/russkiylis/sql-fox',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)