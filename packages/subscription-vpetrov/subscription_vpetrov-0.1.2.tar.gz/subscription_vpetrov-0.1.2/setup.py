"""
Setup file for subscription_utils package
"""
from setuptools import setup, find_packages

setup(
    name='subscription_vpetrov',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'pydantic',
        'sqlalchemy',
        'alembic',
        'email-validator',
        'python-dateutil'
    ]
)
