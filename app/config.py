import os

SECRET_KEY = "8a9d11edee3b7ec7650fc7c68126103f7a0c8d23d996fd57b6c9821364145943"
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = "postgresql://usr:pwd@pgsql:5432/crud"