"""
Setup file for store_utils package
"""
from setuptools import setup, find_packages

setup(
    name='store_vpetrov',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'pydantic',
        'sqlalchemy',
    ]
)
