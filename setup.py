from setuptools import setup, find_packages

requires = [
    'flask',
    'flask-sqlalchemy',
    'psycopg2'
]

setup(
    name='Retrievr',
    version='0.0',
    description='A spotify-like audio management system',
    author='Retriever Labs',
    author_email='',
    keywords='retriever audio web flask free FOSS',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)